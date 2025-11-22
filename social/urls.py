from django.urls import path
from .views import FollowView, BlockView

urlpatterns = [
    path("users/<int:user_id>/follow/", FollowView.as_view(), name="follow"),
    path("users/<int:user_id>/block/", BlockView.as_view(), name="block"),
]
