# Generated by Django 5.1 on 2024-08-15 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_alter_todo_options_remove_todo_title_todo_task_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='task',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='todo',
            name='user',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
