# Generated by Django 5.1.6 on 2025-03-11 10:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_ordenitem_imagen'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orden',
            name='usuario',
        ),
        migrations.AddField(
            model_name='orden',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordenes', to=settings.AUTH_USER_MODEL),
        ),
    ]
