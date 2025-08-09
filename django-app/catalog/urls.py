from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

# API router setup
router = DefaultRouter()
router.register(r'albums', views.AlbumViewSet, basename='album')
router.register(r'songs', views.SongViewSet, basename='song')
router.register(r'tracklist', views.TracklistViewSet, basename='tracklistitem')

urlpatterns = [
    # API Routes
    path('api/', include(router.urls)),
    path('ajax/song/create/', views.create_song_ajax, name='create_song_ajax'),

    # BOP Routes
    path('', views.AlbumListView.as_view(), name='album-list'),
    path('albums/new/', views.AlbumCreateView.as_view(), name='album-create'),
    path('albums/<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='album-edit'),
    path('albums/<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album-delete'),
    path('albums/<int:pk>/', views.AlbumDetailView.as_view(), name='album-detail'),
    path('albums/<int:pk>/<slug:slug>/', views.AlbumDetailView.as_view(), name='album-detail-slug'),

    # Authentication Routes
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True,
        next_page='album-list',
    ), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(
        next_page='album-list'
    ), name='logout'),
    path('accounts/register/', views.register_view, name='register'),
    path('admin/register/', views.admin_register_user, name='admin_register_user'),
]