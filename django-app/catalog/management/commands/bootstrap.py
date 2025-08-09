from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from catalog.models import MusicManagerUser

class Command(BaseCommand):
    help = 'Bootstrap initial data - create groups and permissions'
    
    def handle(self, *args, **options):
        # Create user groups for different roles
        editor_group, created = Group.objects.get_or_create(name='Editor')
        if created:
            self.stdout.write(f'Created group: {editor_group.name}')
        
        artist_group, created = Group.objects.get_or_create(name='Artist')
        if created:
            self.stdout.write(f'Created group: {artist_group.name}')
        
        viewer_group, created = Group.objects.get_or_create(name='Viewer')
        if created:
            self.stdout.write(f'Created group: {viewer_group.name}')
        
        # Set up permissions for each group
        # Editor: all permissions
        editor_permissions = Permission.objects.all()
        editor_group.permissions.set(editor_permissions)
        
        # Artist: view and change permissions for albums (they can edit their own)
        artist_permissions = Permission.objects.filter(
            content_type__app_label='catalog',
            codename__in=['view_album', 'change_album']
        )
        artist_group.permissions.set(artist_permissions)
        
        # Viewer: only view permissions
        viewer_permissions = Permission.objects.filter(
            content_type__app_label='catalog',
            codename__startswith='view'
        )
        viewer_group.permissions.set(viewer_permissions)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully bootstrapped groups and permissions')
        ) 