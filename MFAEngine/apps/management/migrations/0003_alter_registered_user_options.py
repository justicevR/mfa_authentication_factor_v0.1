# Generated by Django 3.2.6 on 2021-11-17 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_registered_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registered_user',
            options={'ordering': ['username', 'last_login', 'status', 'date_joined']},
        ),
    ]