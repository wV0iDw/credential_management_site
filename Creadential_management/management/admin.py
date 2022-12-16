from django.contrib import admin
from .models import CustomUser,Roles

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    # ...
    list_display = ['first_name']
admin.site.register(CustomUser,CustomUserAdmin)

class RolesAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Roles,RolesAdmin)
