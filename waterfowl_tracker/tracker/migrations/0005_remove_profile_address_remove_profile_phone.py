# Generated by Django 4.0.1 on 2022-01-13 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_alter_profile_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='phone',
        ),
    ]