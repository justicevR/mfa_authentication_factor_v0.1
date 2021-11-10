from django.db import models
from django.db.models.enums import Choices
from config import settings
from ..users.models import User
# Create your models here.


class ApplicationRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    developer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(app_label)s_%(class)s",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    name_of_app = models.CharField(max_length=255, blank=True)
    domain = models.CharField(max_length=100, unique=True)
    org_name = models.CharField(max_length=200)

    redirect_uris = models.TextField(
        blank=True,
        help_text= ("Allowed URIs list, space separated")
    )


    claim_of_property = models.TextField(
        blank=False,
        help_text= ("Proof of property, space separated")
    )

    date_requested = models.DateTimeField(auto_now_add=True)

    

    status = models.IntegerField(default=0)

    def __str__(self):
        return self.name_of_app

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200, unique=True, null=True)
    phone = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
	    return self.username







    

    
