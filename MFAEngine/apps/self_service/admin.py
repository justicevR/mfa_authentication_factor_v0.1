from django.contrib import admin

# Register your models here.


from .models import ApplicationRequest, Profile


admin.site.register(ApplicationRequest)
admin.site.register(Profile)
