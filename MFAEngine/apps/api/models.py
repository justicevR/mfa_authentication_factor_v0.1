from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField
import uuid
from oauth2_provider.models import AbstractApplication
from apps.users.models import User

# Create your models here.


class App(AbstractApplication):
    id = models.CharField(max_length=255, primary_key=True)
    api_key = models.CharField(max_length=255, unique=True, null=True)
    domain = models.CharField(max_length=100, unique=True)
    org_name = models.CharField(max_length=200)

    class Meta:
        ordering = ['org_name', 'domain']

    def __str__(self):
        return f'{self.org_name}, {self.domain}'


class UserEnrolled(models.Model):
    user_id = models.CharField(primary_key=True, max_length=255)
    account_name = models.CharField(max_length=100, unique=True)
    app_id = models.ForeignKey(App, on_delete=models.CASCADE, null=True)
    factory = models.CharField(max_length=255, null=True)
    secret = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ['account_name']

    def __str__(self):
        return f'{self.user_id}, {self.account_name}'


class Enrollment(models.Model):
    enrollment_id = models.CharField(primary_key=True, max_length=255)
    enabled = models.BooleanField(default=True)
    validated = models.BooleanField(default=False)
    b64_QRCode = models.TextField() #Base64 encoded QRCode of a generated URI link.
    user_id = models.ForeignKey(UserEnrolled, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['enrollment_id', 'user_id', 'validated', 'created', 'updated']

    def __str__(self):
        return f'{self.enrollment_id}, {self.user_id}'


class BackupCode(models.Model):
    code_id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=100, unique=True)
    expired = models.BooleanField(default=False)
    enrollment_id = models.ForeignKey(Enrollment, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        ordering = ['code_id', 'code', 'expired']

    def __str__(self):
        return f'{self.code}, {self.expired}'