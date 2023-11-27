from django.urls import path
from notification.views import NotificationListView, ReadNotificationView

urlpatterns = [
    path('list/', NotificationListView.as_view(), name='notifications-list'),
    path('read/<int:pk>/', ReadNotificationView.as_view(), name='notifications-read')
]