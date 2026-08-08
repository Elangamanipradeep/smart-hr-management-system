from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

app_name = "accounts"

urlpatterns = [
    # path("login/", views.login_view, name="login"),
    # path("logout/", views.logout_view, name="logout"),
    
    # REST Framework url
    path("register/", views.register_api, name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", views.profile_api, name="profile"),
    path("change-password/", views.ChangePasswordAPIView.as_view(),
    name="change-password",
),
    path(
    "logout/",
    views.LogoutAPIView.as_view(),
    name="logout",
),
]