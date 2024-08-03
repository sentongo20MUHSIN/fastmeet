# Generated by Django 5.0.6 on 2024-06-27 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_alter_tablemeeting_create'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablemeeting',
            name='email',
            field=models.EmailField(default='muhsin@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tablemeeting',
            name='name',
            field=models.CharField(default='muhsin', max_length=100),
            preserve_default=False,
        ),
        
    ]