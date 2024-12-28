# Generated by Django 5.1.4 on 2024-12-23 08:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def assign_default_owner(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Property = apps.get_model('AdminApp', 'Property')  # Replace `your_app_name` with your app's name.

    # Get the first superuser
    admin_user = User.objects.filter(is_superuser=True).first()

    if admin_user:
        # Assign all properties without an owner to the superuser
        Property.objects.filter(owner__isnull=True).update(owner=admin_user)

class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0005_property_latitude_property_longitude'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='properties', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(assign_default_owner),
    ]