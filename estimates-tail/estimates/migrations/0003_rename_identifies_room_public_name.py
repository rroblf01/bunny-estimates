# Generated by Django 5.1.6 on 2025-02-26 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estimates', '0002_task_remove_topic_description_remove_topic_title_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='identifies',
            new_name='public_name',
        ),
    ]
