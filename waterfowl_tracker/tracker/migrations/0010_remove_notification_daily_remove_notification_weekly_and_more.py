# Generated by Django 4.0 on 2022-01-16 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_alter_farmloc_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='daily',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='weekly',
        ),
        migrations.AddField(
            model_name='notification',
            name='interval',
            field=models.CharField(choices=[('Always', 'Always'), ('Detect', 'Only when waterfowl are detected')], default='Always', max_length=50, verbose_name='Waterfowl Presence'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='reportfreq',
            field=models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly')], default='daily', max_length=50, verbose_name='Report Frequency'),
            preserve_default=False,
        ),
    ]
