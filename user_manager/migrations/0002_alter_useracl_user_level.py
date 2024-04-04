# Generated by Django 5.0.3 on 2024-04-04 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useracl',
            name='user_level',
            field=models.PositiveIntegerField(choices=[(10, 'Viewer'), (20, 'Backup Operator'), (30, 'Host Manager'), (40, 'configuration Manager'), (50, 'Administrator')], default=0),
        ),
    ]