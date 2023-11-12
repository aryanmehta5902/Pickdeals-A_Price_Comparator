from django.contrib import admin
from .models import User, Product
# Register your models here.
# admin.site.register(User)


class AdminUser(admin.ModelAdmin):
    def name(self, obj):
        return str(obj)
    name.short_description = 'Name'

    def verified(self, obj):
        return obj.otp == ''
    verified.boolean = True
    verified.short_description = 'OTP Verified'

    list_display = ('username',  'mobile_no', 'address')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    search_fields = ['username', 'mobile_no', 'address']

admin.site.register(Product)
admin.site.register(User, AdminUser)