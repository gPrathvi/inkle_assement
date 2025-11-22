from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupView, MeView, PromoteAdminView, DemoteAdminView, UserSearchView

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("users/me/", MeView.as_view(), name="me"),
    path("users/search/", UserSearchView.as_view(), name="user_search"),
    path("owner/admins/<int:user_id>/", PromoteAdminView.as_view(), name="promote_admin"),
    path("owner/admins/<int:user_id>/demote/", DemoteAdminView.as_view(), name="demote_admin"),
]
