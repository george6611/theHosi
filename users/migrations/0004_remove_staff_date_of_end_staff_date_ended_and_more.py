# Generated by Django 5.0.3 on 2024-03-24 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_departments_in_charge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='date_of_end',
        ),
        migrations.AddField(
            model_name='staff',
            name='date_ended',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='staff',
            name='department',
            field=models.CharField(default='', max_length=50),
        ),
    ]
