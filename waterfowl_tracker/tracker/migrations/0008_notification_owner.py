# Generated by Django 4.0 on 2022-01-14 00:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('tracker', '0007_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user'),
        ),
    ]
