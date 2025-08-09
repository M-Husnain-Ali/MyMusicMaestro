from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from catalog.models import MusicManagerUser, Album, Song, AlbumTracklistItem
from datetime import date, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seed database with sample data for testing'
    
    def handle(self, *args, **options):
        # Create sample users
        editor_group = Group.objects.get(name='Editor')
        artist_group = Group.objects.get(name='Artist')
        viewer_group = Group.objects.get(name='Viewer')
        
        # Create editor user
        editor_user, created = MusicManagerUser.objects.get_or_create(
            username='editor',
            defaults={
                'display_name': 'Music Editor',
                'role': 'editor',
                'is_staff': True,
            }
        )
        if created:
            editor_user.set_password('editor123')
            editor_user.save()
            editor_user.groups.add(editor_group)
            self.stdout.write(f'Created editor user: {editor_user.username}')
        
        # Create artist user
        artist_user, created = MusicManagerUser.objects.get_or_create(
            username='artist',
            defaults={
                'display_name': 'The Beatles',
                'role': 'artist',
            }
        )
        if created:
            artist_user.set_password('artist123')
            artist_user.save()
            artist_user.groups.add(artist_group)
            self.stdout.write(f'Created artist user: {artist_user.username}')
        
        # Create viewer user
        viewer_user, created = MusicManagerUser.objects.get_or_create(
            username='viewer',
            defaults={
                'display_name': 'Music Viewer',
                'role': 'viewer',
            }
        )
        if created:
            viewer_user.set_password('viewer123')
            viewer_user.save()
            viewer_user.groups.add(viewer_group)
            self.stdout.write(f'Created viewer user: {viewer_user.username}')
        
        # Create sample albums
        album1, created = Album.objects.get_or_create(
            title='Abbey Road',
            artist='The Beatles',
            format='vi',
            defaults={
                'description': 'The eleventh studio album by the English rock band The Beatles.',
                'price': Decimal('25.99'),
                'release_date': date(1969, 9, 26),
            }
        )
        if created:
            self.stdout.write(f'Created album: {album1.title}')
        
        album2, created = Album.objects.get_or_create(
            title='Dark Side of the Moon',
            artist='Pink Floyd',
            format='cd',
            defaults={
                'description': 'The eighth studio album by the English rock band Pink Floyd.',
                'price': Decimal('15.99'),
                'release_date': date(1973, 3, 1),
            }
        )
        if created:
            self.stdout.write(f'Created album: {album2.title}')
        
        # Create sample songs
        song1, created = Song.objects.get_or_create(
            title='Come Together',
            defaults={'running_time': 259}  # 4:19
        )
        if created:
            self.stdout.write(f'Created song: {song1.title}')
        
        song2, created = Song.objects.get_or_create(
            title='Something',
            defaults={'running_time': 183}  # 3:03
        )
        if created:
            self.stdout.write(f'Created song: {song2.title}')
        
        song3, created = Song.objects.get_or_create(
            title='Time',
            defaults={'running_time': 413}  # 6:53
        )
        if created:
            self.stdout.write(f'Created song: {song3.title}')
        
        # Create tracklist items
        track1, created = AlbumTracklistItem.objects.get_or_create(
            album=album1,
            song=song1,
            defaults={'position': 1}
        )
        if created:
            self.stdout.write(f'Added {song1.title} to {album1.title}')
        
        track2, created = AlbumTracklistItem.objects.get_or_create(
            album=album1,
            song=song2,
            defaults={'position': 2}
        )
        if created:
            self.stdout.write(f'Added {song2.title} to {album1.title}')
        
        track3, created = AlbumTracklistItem.objects.get_or_create(
            album=album2,
            song=song3,
            defaults={'position': 1}
        )
        if created:
            self.stdout.write(f'Added {song3.title} to {album2.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with sample data')
        ) 