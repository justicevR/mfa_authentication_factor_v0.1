# Generated by Django 3.2.6 on 2021-09-01 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210901_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
