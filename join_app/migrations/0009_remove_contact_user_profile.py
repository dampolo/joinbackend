# Generated by Django 5.1.7 on 2025-06-08 20:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('join_app', '0008_alter_contact_user_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='user_profile',
        ),
    ]
