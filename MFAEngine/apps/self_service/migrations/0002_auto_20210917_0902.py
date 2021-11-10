# Generated by Django 3.2.6 on 2021-09-17 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('self_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationrequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Rejected', 'Rejected'), ('Registered', 'Registered')], max_length=30, null=True),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
