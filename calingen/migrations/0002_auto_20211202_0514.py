# Generated by Django 3.2.9 on 2021-12-02 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calingen', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='type',
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.CharField(choices=[('ANNUAL_ANNIVERSARY', 'Annual Anniversary'), ('HOLIDAY', 'Holiday')], default='ANNUAL_ANNIVERSARY', help_text='The category of this event.', max_length=18, verbose_name='Event Category'),
        ),
    ]