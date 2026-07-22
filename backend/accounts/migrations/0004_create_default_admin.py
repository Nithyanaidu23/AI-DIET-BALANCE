from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_default_admin(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
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
                'password': make_password(admin['password']),
                'first_name': admin['first_name'],
                'last_name': admin['last_name'],
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )
        if not created:
            user.password = make_password(admin['password'])
            user.first_name = admin['first_name']
            user.last_name = admin['last_name']
            user.role = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_subscription_payment'),
    ]

    operations = [
        migrations.RunPython(create_default_admin, reverse_code=migrations.RunPython.noop),
    ]
