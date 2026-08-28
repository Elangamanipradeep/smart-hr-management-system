from django.urls import path
from . import api_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

app_name = "accounts"

urlpatterns = [
    
    # REST Framework url
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", api_views.profile_api, name="profile"),
    path("change-password/", api_views.ChangePasswordAPIView.as_view(),
    name="change-password",
),
    path(
        "logout/",
        api_views.LogoutAPIView.as_view(),
        name="logout",
    ),
    path(
        "users/",
        api_views.HRUserListCreateAPIView.as_view(),
        name="user-list-create",
    ),
    path(
        "users/<int:pk>/",
        api_views.HRUserRetrieveUpdateDestroyAPIView.as_view(),
        name="user-detail",
    ),
]