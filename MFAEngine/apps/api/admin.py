from apps.api.models import Enrollment, App, UserEnrolled, BackupCode
from django.contrib import admin

# Register your models here.


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_id', 'enabled', 'validated', 'b64_QRCode')

class UserEnrolledAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'account_name', 'factory', 'secret')

class BackupCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'expired')

admin.site.register(UserEnrolled, UserEnrolledAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(BackupCode, BackupCodeAdmin)
