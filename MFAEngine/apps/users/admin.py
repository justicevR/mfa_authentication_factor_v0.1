from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_admin')


admin.site.register(User, UserAdmin)