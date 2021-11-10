# Generated by Django 3.2.6 on 2021-09-01 14:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    run_before = [
        ('oauth2_provider', '0001_initial'),
    ]
    
    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('user_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('api_key', models.CharField(max_length=255, null=True, unique=True)),
                ('domain', models.CharField(max_length=100, unique=True)),
                ('org_name', models.CharField(max_length=200)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
            ],
            options={
                'ordering': ['org_name', 'domain'],
            },
        ),
        migrations.CreateModel(
            name='TokenConfig',
            fields=[
                ('config_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('token_type', models.CharField(max_length=5)),
                ('algorithm', models.CharField(max_length=7)),
                ('digits', models.IntegerField()),
                ('period', models.IntegerField()),
                ('period_skew', models.IntegerField()),
            ],
            options={
                'ordering': ['config_id', 'token_type'],
            },
        ),
        migrations.CreateModel(
            name='UserEnrolled',
            fields=[
                ('user_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('account_name', models.CharField(max_length=100, unique=True)),
                ('app_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.app')),
            ],
            options={
                'ordering': ['account_name'],
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('enrollment_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('enabled', models.BooleanField(default=True)),
                ('validated', models.BooleanField(default=False)),
                ('b64_QRCode', models.TextField()),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.tokenconfig')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userenrolled')),
            ],
            options={
                'ordering': ['enrollment_id', 'user_id', 'validated', 'created', 'updated'],
            },
        ),
        migrations.CreateModel(
            name='BackupCode',
            fields=[
                ('code_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('expired', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('enrollment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.enrollment')),
            ],
        ),
        migrations.AddField(
            model_name='app',
            name='config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.tokenconfig'),
        ),
        migrations.AddField(
            model_name='app',
            name='uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
