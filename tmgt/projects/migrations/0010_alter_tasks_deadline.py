# Generated by Django 3.2.5 on 2021-07-21 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_alter_tasks_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]
