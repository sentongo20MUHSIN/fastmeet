# Generated by Django 5.0.6 on 2024-07-02 14:26


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0006_delete_create_alter_tablemeeting_title'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='tablemeeting',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]