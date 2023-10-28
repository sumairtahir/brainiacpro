from django.urls import path
from . import views

urlpatterns = [
    path('', views.outputs_main_view, name="outputs_main"),
    path('/<slug:feature_slug>', views.output_history, name="output_history"),
    path('/delete-output/<int:output_id>', views.delete_output, name="delete_output"),
]