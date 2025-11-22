from django.urls import path
from .views import FeedView, NotificationListView, NotificationDetailView

urlpatterns = [
    path("feed/", FeedView.as_view(), name="feed"),
    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path("notifications/<int:notif_id>/read/", NotificationDetailView.as_view(), name="notification_read"),
]
