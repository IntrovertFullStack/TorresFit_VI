# Generated by Django 5.1.6 on 2025-03-11 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_rename_user_orden_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user',
            new_name='usuario',
        ),
    ]
