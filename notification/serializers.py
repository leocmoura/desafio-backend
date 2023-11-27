from rest_framework import serializers
from notification.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'message', 'read')

class ReadNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('read', )