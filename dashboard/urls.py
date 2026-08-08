from django.urls import path
from . import views, api_views

app_name = "dashboard"

urlpatterns = [
    path(
        "api/dashboard/",
        api_views.DashboardAPIView.as_view(),
        name="dashboard-api",
    ),
    path("", views.dashboard, name="dashboard"),
]
