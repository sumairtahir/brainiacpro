from django.urls import path
from . import views

urlpatterns = [
    path('', views.features, name="features"),
    path('<slug:feature_slug>', views.feature_view, name="feature"),
    path('document-mode/<str:task>', views.document_mode, name="document_mode"),
    path('star_output/<int:output_id>', views.star_output, name="star_output"),
    path('fav_feature/<int:feature_id>', views.favorite_feature_view, name="favorite_feature"),
]
