# Generated by Django 3.2.9 on 2021-11-18 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(help_text='The start date and time for this recurring event.', verbose_name='Start Date')),
                ('title', models.CharField(help_text='This will be included in the generated output and is capped at 50 characters.', max_length=50, verbose_name='Event Title')),
                ('type', models.CharField(choices=[('ANNUAL_ANNIVERSARY', 'Annual Anniversary')], default='ANNUAL_ANNIVERSARY', help_text='The type of this event.', max_length=18, verbose_name='Event Type')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'unique_together': {('title', 'start')},
            },
        ),
    ]
