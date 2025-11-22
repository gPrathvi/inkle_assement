from django.urls import path
from .views import AdminListUsersView, AdminDeactivateUserView, AdminReactivateUserView, AdminDeletePostView

urlpatterns = [
    path("admin/users/", AdminListUsersView.as_view(), name="admin_list_users"),
    path("admin/users/<int:user_id>/", AdminDeactivateUserView.as_view(), name="admin_deactivate_user"),
    path("admin/users/<int:user_id>/reactivate/", AdminReactivateUserView.as_view(), name="admin_reactivate_user"),
    path("admin/posts/<int:post_id>/", AdminDeletePostView.as_view(), name="admin_delete_post"),
]
