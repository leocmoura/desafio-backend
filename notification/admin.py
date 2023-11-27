from django.contrib import admin
from notification.models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Notification._meta.fields]
    list_display_links = ['id']

admin.site.register(Notification, NotificationAdmin)