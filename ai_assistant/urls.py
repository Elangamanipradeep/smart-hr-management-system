from django.urls import path
from .views import (
    AIAskAPIView,
    AIHRInsightsAPIView,
    AIEmployeeInsightsAPIView,
)

app_name = "ai_assistant"


urlpatterns = [

    path(
        "ask/",
        AIAskAPIView.as_view(),
        name="ai_ask",
    ),
    path(
        "insights/",
        AIHRInsightsAPIView.as_view(),
        name="ai_insights",
    ),
    path(
        "employees/<int:employee_id>/insights/",
        AIEmployeeInsightsAPIView.as_view(),
        name="ai_employee_insights",
    ),

]