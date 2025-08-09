from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import MusicManagerUser, Album, Song, AlbumTracklistItem

# Custom admin site configuration
admin.site.site_header = "🎵 MyMusicMaestro Admin"
admin.site.site_title = "MyMusicMaestro Admin Portal"
admin.site.index_title = "Welcome to MyMusicMaestro Administration"

@admin.register(MusicManagerUser)
class MusicManagerUserAdmin(UserAdmin):
    """Enhanced admin for MusicManagerUser"""
    list_display = ['username', 'display_name', 'role_badge', 'is_active', 'album_count', 'date_joined']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['username', 'display_name', 'email']
    actions = ['activate_users', 'deactivate_users']
    
    fieldsets = UserAdmin.fieldsets + (
        ('🎵 Music Manager Info', {
            'fields': ('display_name', 'role'),
            'classes': ('wide',)
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('🎵 Music Manager Info', {
            'fields': ('display_name', 'role'),
            'classes': ('wide',)
        }),
    )
    
    def role_badge(self, obj):
        """Display role as a colored badge"""
        colors = {
            'editor': '#28a745',
            'artist': '#007bff', 
            'viewer': '#6c757d'
        }
        color = colors.get(obj.role, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color, obj.get_role_display()
        )
    role_badge.short_description = 'Role'
    
    def album_count(self, obj):
        """Show number of albums for artists"""
        if obj.role == 'artist':
            count = Album.objects.filter(artist=obj.display_name).count()
            return f"🎵 {count} albums"
        return "—"
    album_count.short_description = 'Albums'
    
    def activate_users(self, request, queryset):
        """Custom action to activate users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'✅ Successfully activated {updated} users.')
    activate_users.short_description = "✅ Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Custom action to deactivate users"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'❌ Successfully deactivated {updated} users.')
    deactivate_users.short_description = "❌ Deactivate selected users"

class AlbumTracklistItemInline(admin.TabularInline):
    """Enhanced inline admin for tracklist items"""
    model = AlbumTracklistItem
    extra = 1
    ordering = ['position']
    fields = ['position', 'song', 'duration_display']
    readonly_fields = ['duration_display']
    
    def duration_display(self, obj):
        """Display song duration"""
        if obj.song and obj.song.running_time:
            minutes = obj.song.running_time // 60
            seconds = obj.song.running_time % 60
            return f"⏱️ {minutes}:{seconds:02d}"
        return "—"
    duration_display.short_description = 'Duration'

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """Enhanced admin for Album model"""
    list_display = ['cover_thumbnail', 'title', 'artist', 'format_badge', 'release_date', 'price_display', 'track_count', 'view_detail']
    list_filter = ['format', 'release_date', 'artist']
    search_fields = ['title', 'artist', 'description']
    readonly_fields = ['slug', 'cover_preview', 'album_stats']
    inlines = [AlbumTracklistItemInline]
    actions = ['delete_selected_albums', 'export_albums']
    
    fieldsets = (
        ('🎵 Basic Information', {
            'fields': ('title', 'artist', 'description'),
            'classes': ('wide',)
        }),
        ('💿 Album Details', {
            'fields': ('price', 'format', 'release_date', 'cover_image', 'cover_preview'),
            'classes': ('wide',)
        }),
        ('📊 Statistics', {
            'fields': ('album_stats',),
            'classes': ('wide',)
        }),
        ('🔧 System', {
            'fields': ('slug',),
            'classes': ('collapse',)
        })
    )
    
    def cover_thumbnail(self, obj):
        """Display small cover image thumbnail"""
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.cover_image.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px;">🎵</div>'
        )
    cover_thumbnail.short_description = 'Cover'
    
    def cover_preview(self, obj):
        """Display larger cover image preview"""
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);" />',
                obj.cover_image.url
            )
        return format_html(
            '<div style="width: 200px; height: 200px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;">🎵<br/>No Cover</div>'
        )
    cover_preview.short_description = 'Cover Preview'
    
    def format_badge(self, obj):
        """Display format as a colored badge"""
        colors = {
            'dd': '#17a2b8',  # info
            'cd': '#28a745',  # success  
            'vi': '#dc3545'   # danger
        }
        labels = {
            'dd': 'Digital',
            'cd': 'CD',
            'vi': 'Vinyl'
        }
        color = colors.get(obj.format, '#6c757d')
        label = labels.get(obj.format, obj.format)
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">💿 {}</span>',
            color, label
        )
    format_badge.short_description = 'Format'
    
    def price_display(self, obj):
        """Display price with currency symbol"""
        return f"💰 £{obj.price}"
    price_display.short_description = 'Price'
    
    def track_count(self, obj):
        """Display number of tracks"""
        count = obj.tracks.count()
        return f"🎵 {count} tracks"
    track_count.short_description = 'Tracks'
    
    def album_stats(self, obj):
        """Display album statistics"""
        track_count = obj.tracks.count()
        total_time = sum(track.song.running_time for track in obj.tracks.all())
        total_minutes = total_time // 60
        total_seconds = total_time % 60
        
        return format_html(
            '''
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea;">
                <strong>📊 Album Statistics</strong><br/>
                🎵 Tracks: {}<br/>
                ⏱️ Total Duration: {}:{:02d}<br/>
                📅 Release Year: {}<br/>
                🏷️ Slug: <code>{}</code>
            </div>
            ''',
            track_count, total_minutes, total_seconds, obj.release_year, obj.slug
        )
    album_stats.short_description = 'Statistics'
    
    def view_detail(self, obj):
        """Link to view album details"""
        url = reverse('album-detail', args=[obj.pk])
        return format_html(
            '<a href="{}" target="_blank" style="background: #667eea; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none; font-size: 11px;">👁️ View</a>',
            url
        )
    view_detail.short_description = 'Actions'
    
    def delete_selected_albums(self, request, queryset):
        """Custom delete action with confirmation"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'🗑️ Successfully deleted {count} albums.')
    delete_selected_albums.short_description = "🗑️ Delete selected albums"
    
    def export_albums(self, request, queryset):
        """Export albums data"""
        # This would implement CSV export functionality
        self.message_user(request, f'📁 Export functionality coming soon! Selected {queryset.count()} albums.')
    export_albums.short_description = "📁 Export selected albums"

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """Enhanced admin for Song model"""
    list_display = ['title', 'duration_badge', 'album_count', 'created_info']
    search_fields = ['title']
    actions = ['recalculate_durations']
    
    def duration_badge(self, obj):
        """Display duration as a badge"""
        minutes = obj.running_time // 60
        seconds = obj.running_time % 60
        return format_html(
            '<span style="background-color: #17a2b8; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">⏱️ {}:{:02d}</span>',
            minutes, seconds
        )
    duration_badge.short_description = 'Duration'
    
    def album_count(self, obj):
        """Show how many albums this song appears in"""
        count = obj.album_tracks.count()
        return f"💿 {count} albums"
    album_count.short_description = 'Albums'
    
    def created_info(self, obj):
        """Show creation info"""
        return "🆕 New Song"
    created_info.short_description = 'Status'
    
    def recalculate_durations(self, request, queryset):
        """Custom action example"""
        self.message_user(request, f'⏱️ Processed {queryset.count()} songs.')
    recalculate_durations.short_description = "⏱️ Recalculate durations"

@admin.register(AlbumTracklistItem)
class AlbumTracklistItemAdmin(admin.ModelAdmin):
    """Enhanced admin for AlbumTracklistItem"""
    list_display = ['album_link', 'position_badge', 'song_link', 'duration_display']
    list_filter = ['album', 'album__format']
    ordering = ['album', 'position']
    search_fields = ['album__title', 'song__title']
    
    def album_link(self, obj):
        """Link to album"""
        return format_html(
            '<a href="{}" style="color: #667eea; font-weight: bold;">💿 {}</a>',
            reverse('admin:catalog_album_change', args=[obj.album.pk]),
            obj.album.title
        )
    album_link.short_description = 'Album'
    
    def position_badge(self, obj):
        """Display position as a badge"""
        return format_html(
            '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 50%; font-size: 11px; font-weight: bold; min-width: 20px; text-align: center; display: inline-block;">#{}</span>',
            obj.position
        )
    position_badge.short_description = 'Position'
    
    def song_link(self, obj):
        """Link to song"""
        return format_html(
            '<a href="{}" style="color: #764ba2; font-weight: bold;">🎵 {}</a>',
            reverse('admin:catalog_song_change', args=[obj.song.pk]),
            obj.song.title
        )
    song_link.short_description = 'Song'
    
    def duration_display(self, obj):
        """Display song duration"""
        if obj.song.running_time:
            minutes = obj.song.running_time // 60
            seconds = obj.song.running_time % 60
            return format_html(
                '<span style="color: #6c757d; font-family: monospace;">⏱️ {}:{:02d}</span>',
                minutes, seconds
            )
        return "—"
    duration_display.short_description = 'Duration'