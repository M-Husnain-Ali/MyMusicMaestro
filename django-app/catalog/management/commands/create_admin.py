from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class Command(BaseCommand):
    help = 'Create an admin user (editor role) with specified name'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='The display name for the admin user')
        parser.add_argument(
            '--username',
            type=str,
            help='Username (optional, defaults to lowercase name with no spaces)',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email address (optional, defaults to name@admin.com)',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='Password (optional, defaults to "admin123")',
        )

    def handle(self, *args, **options):
        name = options['name']
        username = options['username'] or name.lower().replace(' ', '')
        email = options['email'] or f"{username}@admin.com"
        password = options['password']

        try:
            # Create the admin user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                display_name=name,
                role='editor'  # Admin users have 'editor' role
            )
            
            # Make them a superuser if this is the first admin
            if User.objects.filter(is_superuser=True).count() == 0:
                user.is_superuser = True
                user.is_staff = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created SUPERUSER admin: {name} (username: {username})'
                    )
                )
            else:
                user.is_staff = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created admin user: {name} (username: {username})'
                    )
                )
            
            self.stdout.write(f'Email: {email}')
            self.stdout.write(f'Password: {password}')
            self.stdout.write(f'Role: Editor (Admin)')
            
        except IntegrityError:
            raise CommandError(f'User with username "{username}" already exists')
        except Exception as e:
            raise CommandError(f'Error creating user: {str(e)}') 