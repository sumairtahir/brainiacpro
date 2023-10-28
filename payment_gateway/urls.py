from django.urls import path
from .views import (
    CreateCheckoutSessionView,
    ProductLandingPageView,
    CancelView,
    success_view,
    stripe_webhook
)

urlpatterns = [
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', success_view, name='success'),
    path('webhooks/stripe', stripe_webhook, name='stripe-webhook'),
    path('', ProductLandingPageView.as_view(), name='landing-page'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]