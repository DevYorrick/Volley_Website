# Generated by Django 4.2 on 2023-11-29 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_picture',
        ),
    ]
