# Generated by Django 4.2.1 on 2023-06-06 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='day',
            field=models.CharField(blank=True, choices=[('Monday', 'Monday'), ('Wednesday', 'Wednesday')], max_length=10),
        ),
    ]
