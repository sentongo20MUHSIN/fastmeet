# Generated by Django 5.0.6 on 2024-06-26 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Meeting',
            new_name='MeetingMinute',
        ),
        migrations.RemoveField(
            model_name='attending',
            name='user',
        ),
        migrations.RemoveField(
            model_name='tablemeeting',
            name='creator',
        ),
    ]