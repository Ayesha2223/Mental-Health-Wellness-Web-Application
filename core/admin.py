from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import UserProfile, Badge, Activity

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_mindful_minutes', 'calculate_streak')
    search_fields = ('user__username', 'user__email')

class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'unlocked', 'progress', 'date_unlocked')
    list_filter = ('unlocked',)
    search_fields = ('name', 'user__username')

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('title', 'description', 'user__username')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(Activity, ActivityAdmin)