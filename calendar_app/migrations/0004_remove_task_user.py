# Generated by Django 4.2.10 on 2024-03-11 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_app', '0003_alter_task_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='user',
        ),
    ]
