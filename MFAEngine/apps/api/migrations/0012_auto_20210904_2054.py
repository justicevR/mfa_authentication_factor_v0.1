# Generated by Django 3.2.6 on 2021-09-04 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_userenrolled_factory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='updated',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]