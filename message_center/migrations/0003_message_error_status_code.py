# Generated by Django 5.0.4 on 2024-04-16 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message_center', '0002_alter_messagechannel_channel_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='error_status_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]