from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Album, Song, AlbumTracklistItem
from .serializers import AlbumSerializer, SongSerializer, AlbumTracklistItemSerializer, AlbumDetailSerializer, AlbumCreateUpdateSerializer
from .forms import UserRegistrationForm, AlbumForm, AlbumTracklistItemForm

# BOP (Templated) Views
def register_view(request):
    """Artist registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Role is automatically set to 'artist' in the form
            messages.success(request, f'Artist account created successfully! You can now login to manage your music catalog.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {
        'form': form,
        'title': 'Register as Artist'
    })

@login_required
def admin_register_user(request):
    """Admin-only user registration view"""
    if not request.user.is_superuser:
        raise PermissionDenied("You do not have permission to register users.")
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('admin:catalog_musicmanageruser_changelist')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'admin/catalog/register_user.html', {
        'form': form,
        'title': 'Register New User'
    })

class AlbumListView(ListView):
    """List all albums, filtered by artist if user is an artist"""
    model = Album
    template_name = 'catalog/album_list.html'
    context_object_name = 'albums'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.role == 'artist':
            return queryset.filter(artist__iexact=self.request.user.display_name)
        return queryset

class AlbumDetailView(DetailView):
    """Display album details"""
    model = Album
    template_name = 'catalog/album_detail.html'
    context_object_name = 'album'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = self.get_object()
        user = self.request.user
        
        # Check if user can edit (case-insensitive)
        can_edit = (user.is_authenticated and 
                   (user.role == 'editor' or 
                    (user.role == 'artist' and album.artist.lower() == user.display_name.lower())))
        
        # Check if user can delete (editors only)
        can_delete = user.is_authenticated and user.role == 'editor'
        
        context['can_edit'] = can_edit
        context['can_delete'] = can_delete
        
        return context

class AlbumCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create a new album (editors only)"""
    model = Album
    form_class = AlbumForm
    template_name = 'catalog/album_form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        TracklistItemFormSet = inlineformset_factory(
            Album,
            AlbumTracklistItem,
            form=AlbumTracklistItemForm,
            extra=0,
            can_delete=True
        )
        if self.request.POST:
            formset = TracklistItemFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            formset = TracklistItemFormSet(instance=self.object)
        data['tracklist_formset'] = formset
        data['tracklist_has_errors'] = formset.total_error_count() > 0
        data['songs'] = Song.objects.all()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tracklist_formset = context['tracklist_formset']
        if tracklist_formset.is_valid():
            self.object = form.save()
            tracklist_formset.instance = self.object
            tracklist_formset.save()
            messages.success(self.request, "Album created successfully!")
            return redirect('album-detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        return self.request.user.role in ['editor', 'artist']

class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing album (editors or album's artist)"""
    model = Album
    form_class = AlbumForm
    template_name = 'catalog/album_form.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        TracklistItemFormSet = inlineformset_factory(
            Album,
            AlbumTracklistItem,
            form=AlbumTracklistItemForm,
            extra=0,
            can_delete=True
        )
        if self.request.POST:
            formset = TracklistItemFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            formset = TracklistItemFormSet(instance=self.object)
        data['tracklist_formset'] = formset
        data['tracklist_has_errors'] = formset.total_error_count() > 0
        data['songs'] = Song.objects.all()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        tracklist_formset = context['tracklist_formset']
        if tracklist_formset.is_valid():
            self.object = form.save()
            tracklist_formset.instance = self.object
            tracklist_formset.save()
            messages.success(self.request, "Album updated successfully!")
            return redirect('album-detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        album = self.get_object()
        return (self.request.user.role == 'editor' or 
                (self.request.user.role == 'artist' and album.artist.lower() == self.request.user.display_name.lower()))

class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an album (editors only)"""
    model = Album
    template_name = 'catalog/album_confirm_delete.html'
    success_url = reverse_lazy('album-list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role != 'editor':
            messages.error(request, 'Only editors can delete albums.')
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Album deleted successfully!')
        return super().delete(request, *args, **kwargs)


# API Views
class AlbumViewSet(viewsets.ModelViewSet):
    """API endpoint for albums"""
    queryset = Album.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AlbumSerializer
        if self.action == 'retrieve':
            return AlbumDetailSerializer
        return AlbumCreateUpdateSerializer # For create, update, partial_update

    def get_permissions(self):
        """No auth for read, auth for write"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class SongViewSet(viewsets.ModelViewSet):
    """API endpoint for songs"""
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [AllowAny] # Per spec

class TracklistViewSet(viewsets.ModelViewSet):
    """API endpoint for tracklist items"""
    queryset = AlbumTracklistItem.objects.all()
    serializer_class = AlbumTracklistItemSerializer
    permission_classes = [AllowAny] # Per spec

@login_required
def create_song_ajax(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        running_time = request.POST.get('running_time', '').strip()
        
        if not title or not running_time:
            return JsonResponse({
                'success': False, 
                'error': 'Both title and running time are required.'
            }, status=400)
            
        try:
            running_time = int(running_time)
            if running_time < 10:
                return JsonResponse({
                    'success': False, 
                    'error': 'Running time must be at least 10 seconds.'
                }, status=400)
        except ValueError:
            return JsonResponse({
                'success': False, 
                'error': 'Running time must be a valid number.'
            }, status=400)

        # Check if song with this title already exists
        existing_song = Song.objects.filter(title__iexact=title).first()
        if existing_song:
            return JsonResponse({
                'success': False, 
                'error': f'A song with the title "{title}" already exists.'
            }, status=400)

        try:
            song = Song.objects.create(title=title, running_time=running_time)
            return JsonResponse({
                'success': True, 
                'song': {
                    'id': song.id, 
                    'title': song.title,
                    'running_time': song.running_time,
                    'formatted_time': f"{song.running_time // 60}:{song.running_time % 60:02d}"
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': f'Error creating song: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)