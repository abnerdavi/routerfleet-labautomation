# Generated by Django 5.0.7 on 2024-07-09 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backup', '0007_backupprofile_profile_error_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backupprofile',
            name='backup_interval',
            field=models.IntegerField(choices=[(0, 'No interval'), (5, '5 seconds'), (60, '1 minute')], default=0),
        ),
    ]
