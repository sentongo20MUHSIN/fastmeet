# Generated by Django 5.0.6 on 2024-07-15 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0012_tablemeeting_created_by_tablemeeting_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablemeeting',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]