from django.contrib import admin
from .models import Profile, Log,Menu
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('userid','name', 'status', 'points', 'created_at')
    search_fields = ('name__username', 'status')

    def userid(self,obj):
        return obj.name.id
    userid.short_description = 'User ID'

class LogAdmin(admin.ModelAdmin):
    list_display = ('userid','account', 'action', 'date', 'time')
    search_fields = ('account__name__username', 'action')
    list_filter = ('action', 'date')

    def userid(self, obj):
        return obj.account.name.id
    userid.short_description = 'User ID'

class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name','description', 'price')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Menu, MenuAdmin)