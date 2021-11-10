# Generated by Django 3.2.6 on 2021-09-01 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import oauth2_provider.generators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_rename_myapp_app'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='uid',
        ),
        migrations.RemoveField(
            model_name='app',
            name='user_id',
        ),
        migrations.AddField(
            model_name='app',
            name='algorithm',
            field=models.CharField(blank=True, choices=[('', 'No OIDC support'), ('RS256', 'RSA with SHA-2 256'), ('HS256', 'HMAC with SHA-2 256')], default='', max_length=5),
        ),
        migrations.AddField(
            model_name='app',
            name='authorization_grant_type',
            field=models.CharField(choices=[('authorization-code', 'Authorization code'), ('implicit', 'Implicit'), ('password', 'Resource owner password-based'), ('client-credentials', 'Client credentials'), ('openid-hybrid', 'OpenID connect hybrid')], default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='app',
            name='client_id',
            field=models.CharField(db_index=True, default=oauth2_provider.generators.generate_client_id, max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='app',
            name='client_secret',
            field=models.CharField(blank=True, db_index=True, default=oauth2_provider.generators.generate_client_secret, max_length=255),
        ),
        migrations.AddField(
            model_name='app',
            name='client_type',
            field=models.CharField(choices=[('confidential', 'Confidential'), ('public', 'Public')], default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='app',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='app',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='app',
            name='redirect_uris',
            field=models.TextField(blank=True, help_text='Allowed URIs list, space separated'),
        ),
        migrations.AddField(
            model_name='app',
            name='skip_authorization',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='app',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_app', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='app',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='app',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]