from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import UserProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Ensures administrator accounts are created and configured with correct staff privileges.'

    def handle(self, *args, **options):
        admins = [
            {
                'email': '123456@gmail.com',
                'password': '123456',
                'first_name': 'Admin',
                'last_name': 'Developer',
            },
            {
                'email': 'nithyaserala545@gmail.com',
                'password': '123nithya@',
                'first_name': 'nithya',
                'last_name': '',
            },
            {
                'email': 'polaiahmallam8@gmail.com',
                'password': 'Mganesh@701',
                'first_name': 'Ganesh',
                'last_name': '',
            },
        ]

        for admin in admins:
            user, created = User.objects.get_or_create(
                email=admin['email'],
                defaults={
                    'first_name': admin['first_name'],
                    'last_name': admin['last_name'],
                    'role': 'admin',
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True,
                }
            )
            user.set_password(admin['password'])
            user.first_name = admin['first_name']
            user.last_name = admin['last_name']
            user.role = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()

            # Ensure profile exists
            UserProfile.objects.get_or_create(user=user)

            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} administrator account: {admin['email']}"))
