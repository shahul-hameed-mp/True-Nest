# Generated by Django 5.1.4 on 2024-12-15 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0002_property_baths_property_beds_property_garage'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='property_for',
            field=models.CharField(choices=[('for sell', 'For Sell'), ('for rent', 'For Rent')], default='for sell', max_length=20),
            preserve_default=False,
        ),
    ]
