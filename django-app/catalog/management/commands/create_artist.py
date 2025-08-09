from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class Command(BaseCommand):
    help = 'Create an artist user with specified name'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='The artist name (display name)')
        parser.add_argument(
            '--username',
            type=str,
            help='Username (optional, defaults to lowercase name with no spaces)',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email address (optional, defaults to name@artist.com)',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='artist123',
            help='Password (optional, defaults to "artist123")',
        )

    def handle(self, *args, **options):
        name = options['name']
        username = options['username'] or name.lower().replace(' ', '')
        email = options['email'] or f"{username}@artist.com"
        password = options['password']

        try:
            # Create the artist user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                display_name=name,
                role='artist'
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created artist: {name} (username: {username})'
                )
            )
            self.stdout.write(f'Email: {email}')
            self.stdout.write(f'Password: {password}')
            self.stdout.write(f'Role: Artist')
            self.stdout.write('')
            self.stdout.write(
                self.style.WARNING(
                    f'The artist "{name}" can now:'
                )
            )
            self.stdout.write('  • Create and edit their own albums')
            self.stdout.write('  • Add songs to their albums')
            self.stdout.write('  • View only their own albums in the backend')
            
        except IntegrityError:
            raise CommandError(f'User with username "{username}" already exists')
        except Exception as e:
            raise CommandError(f'Error creating artist: {str(e)}') 