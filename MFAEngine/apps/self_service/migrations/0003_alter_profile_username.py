# Generated by Django 3.2.6 on 2021-09-18 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('self_service', '0002_auto_20210917_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]