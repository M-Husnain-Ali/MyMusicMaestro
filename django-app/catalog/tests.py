from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group
from catalog.models import MusicManagerUser, Album, Song, AlbumTracklistItem
from datetime import date, timedelta
from decimal import Decimal

class MusicManagerUserModelTest(TestCase):
    def setUp(self):
        self.user = MusicManagerUser.objects.create_user(
            username='testuser',
            password='testpass123',
            display_name='Test User',
            role='editor'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.display_name, 'Test User')
        self.assertEqual(self.user.role, 'editor')
        self.assertEqual(str(self.user), 'Test User')

class AlbumModelTest(TestCase):
    def setUp(self):
        self.album = Album.objects.create(
            title='Test Album',
            artist='Test Artist',
            format='cd',
            price=Decimal('15.99'),
            release_date=date.today(),
            description='Test description'
        )
    
    def test_album_creation(self):
        self.assertEqual(self.album.title, 'Test Album')
        self.assertEqual(self.album.artist, 'Test Artist')
        self.assertEqual(self.album.format, 'cd')
        self.assertEqual(self.album.price, Decimal('15.99'))
        self.assertTrue(self.album.slug)
    
    def test_album_str(self):
        self.assertEqual(str(self.album), 'Test Album by Test Artist')
    
    def test_short_description_property(self):
        long_desc = 'A' * 150
        self.album.description = long_desc
        self.album.save()
        self.assertEqual(len(self.album.short_description), 103)  # 100 + '...'
    
    def test_release_year_property(self):
        self.assertEqual(self.album.release_year, date.today().year)
    
    def test_slug_auto_generation(self):
        album2 = Album.objects.create(
            title='Another Album',
            artist='Another Artist',
            format='vi',
            price=Decimal('25.99'),
            release_date=date.today()
        )
        self.assertTrue(album2.slug)
        self.assertIn('another-album', album2.slug)

class SongModelTest(TestCase):
    def setUp(self):
        self.song = Song.objects.create(
            title='Test Song',
            running_time=180  # 3 minutes
        )
    
    def test_song_creation(self):
        self.assertEqual(self.song.title, 'Test Song')
        self.assertEqual(self.song.running_time, 180)
        self.assertEqual(str(self.song), 'Test Song')
    
    def test_minimum_running_time_validation(self):
        # Test that songs with less than 10 seconds fail validation
        from django.core.exceptions import ValidationError
        song = Song(title='Short Song', running_time=5)
        with self.assertRaises(ValidationError):
            song.full_clean()

class AlbumTracklistItemTest(TestCase):
    def setUp(self):
        self.album = Album.objects.create(
            title='Test Album',
            artist='Test Artist',
            format='cd',
            price=Decimal('15.99'),
            release_date=date.today()
        )
        self.song = Song.objects.create(
            title='Test Song',
            running_time=180
        )
        self.track = AlbumTracklistItem.objects.create(
            album=self.album,
            song=self.song,
            position=1
        )
    
    def test_tracklist_item_creation(self):
        self.assertEqual(self.track.album, self.album)
        self.assertEqual(self.track.song, self.song)
        self.assertEqual(self.track.position, 1)

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create groups
        self.editor_group = Group.objects.create(name='Editor')
        self.artist_group = Group.objects.create(name='Artist')
        self.viewer_group = Group.objects.create(name='Viewer')
        
        # Create users
        self.editor = MusicManagerUser.objects.create_user(
            username='editor',
            password='testpass123',
            display_name='Editor User',
            role='editor'
        )
        self.editor.groups.add(self.editor_group)
        
        self.artist = MusicManagerUser.objects.create_user(
            username='artist',
            password='testpass123',
            display_name='Artist User',
            role='artist'
        )
        self.artist.groups.add(self.artist_group)
        
        self.viewer = MusicManagerUser.objects.create_user(
            username='viewer',
            password='testpass123',
            display_name='Viewer User',
            role='viewer'
        )
        self.viewer.groups.add(self.viewer_group)
        
        # Create test album
        self.album = Album.objects.create(
            title='Test Album',
            artist='Artist User',
            format='cd',
            price=Decimal('15.99'),
            release_date=date.today()
        )
    
    def test_album_list_view_authenticated(self):
        self.client.login(username='editor', password='testpass123')
        response = self.client.get(reverse('album-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Album')
    
    def test_album_list_view_unauthenticated(self):
        response = self.client.get(reverse('album-list'))
        self.assertEqual(response.status_code, 200)  # Should work for unauthenticated users
    
    def test_album_detail_view(self):
        response = self.client.get(reverse('album-detail', kwargs={'pk': self.album.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Album')
    
    def test_album_create_view_editor(self):
        self.client.login(username='editor', password='testpass123')
        response = self.client.get(reverse('album-create'))
        self.assertEqual(response.status_code, 200)
    
    def test_album_create_view_artist_allowed(self):
        self.client.login(username='artist', password='testpass123')
        response = self.client.get(reverse('album-create'))
        self.assertEqual(response.status_code, 200)  # Artists can now create albums
    
    def test_album_edit_view_artist_own_album(self):
        self.client.login(username='artist', password='testpass123')
        response = self.client.get(reverse('album-edit', kwargs={'pk': self.album.pk}))
        self.assertEqual(response.status_code, 200)  # Artist can edit their own album
    
    def test_album_delete_view_editor(self):
        self.client.login(username='editor', password='testpass123')
        response = self.client.get(reverse('album-delete', kwargs={'pk': self.album.pk}))
        self.assertEqual(response.status_code, 200)
    
    def test_album_delete_view_artist_forbidden(self):
        self.client.login(username='artist', password='testpass123')
        response = self.client.get(reverse('album-delete', kwargs={'pk': self.album.pk}))
        self.assertEqual(response.status_code, 403)  # Artists cannot delete albums

class APIViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.album = Album.objects.create(
            title='API Test Album',
            artist='API Artist',
            format='cd',
            price=Decimal('19.99'),
            release_date=date.today()
        )
    
    def test_api_albums_list(self):
        response = self.client.get('/api/albums/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'API Test Album')
    
    def test_api_album_detail(self):
        response = self.client.get(f'/api/albums/{self.album.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'API Test Album')
    
    def test_api_songs_list(self):
        response = self.client.get('/api/songs/')
        self.assertEqual(response.status_code, 200)
    
    def test_api_tracklist(self):
        response = self.client.get('/api/tracklist/')
        self.assertEqual(response.status_code, 200)

class ValidationTest(TestCase):
    def test_album_price_validation(self):
        # Test price cannot be negative
        from django.core.exceptions import ValidationError
        album = Album(
            title='Test Album',
            artist='Test Artist',
            format='cd',
            price=Decimal('-5.99'),
            release_date=date.today()
        )
        with self.assertRaises(ValidationError):
            album.full_clean()
        
        # Test price cannot exceed 999.99
        album.price = Decimal('1000.00')
        with self.assertRaises(ValidationError):
            album.full_clean()
    
    def test_release_date_validation(self):
        from django.core.exceptions import ValidationError
        # Test release date cannot be more than 3 years in future
        future_date = date.today() + timedelta(days=4*365)  # 4 years
        album = Album(
            title='Future Album',
            artist='Future Artist',
            format='dd',
            price=Decimal('9.99'),
            release_date=future_date
        )
        with self.assertRaises(ValidationError):
            album.full_clean()
