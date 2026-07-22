import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth import get_user_model
from users.models import UserProfile

User = get_user_model()

def seed_admins():
    admins = [
        {
            'email': '123456@gmail.com',
            'password': '12345678',
            'first_name': 'Admin',
            'last_name': 'Developer',
        },
        {
            'email': 'nithyaserala545@gmail.com',
            'password': '123nithya@',
            'first_name': 'Nithya',
            'last_name': 'Serala',
        },
        {
            'email': 'polaiahmallam8@gmail.com',
            'password': 'Mganesh@701',
            'first_name': 'Ganesh',
            'last_name': 'Mallam',
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

        UserProfile.objects.get_or_create(user=user)
        status = "Created" if created else "Updated password for"
        print(f"✅ {status} admin account: {admin['email']} / password: {admin['password']}")

if __name__ == '__main__':
    seed_admins()
