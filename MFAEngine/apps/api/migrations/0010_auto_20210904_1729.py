# Generated by Django 3.2.6 on 2021-09-04 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20210904_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenconfig',
            name='algorithm',
            field=models.CharField(default='SHA1', max_length=7),
        ),
        migrations.AlterField(
            model_name='tokenconfig',
            name='token_type',
            field=models.CharField(default='HOTP', max_length=5),
        ),
    ]