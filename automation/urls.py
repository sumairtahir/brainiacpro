from django.urls import path
from . import views

urlpatterns = [
    path('', views.automation_view, name="automation"),
    path('<slug:automation_slug>', views.automation_view, name="automation_view"),
    path('get-operation-settings/<int:operation_id>', views.get_operation_settings, name="get_operation_settings"),
    path("edit-operation-settings/<int:operation_id>", views.edit_operation_settings, name="edit_operation_settings"),
    path("test-channels/", views.test_channels, name="test_channels"),
]
