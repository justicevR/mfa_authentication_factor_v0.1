# Generated by Django 3.2.6 on 2021-09-01 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_app_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='backupcode',
            options={'ordering': ['code_id', 'code', 'expired']},
        ),
    ]
