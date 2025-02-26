from django.urls import path
from .views import (
    CreateStripeProductView,
    CreateStripePriceView,
    CreateCheckoutSessionView,
)

app_name = 'payments'

urlpatterns = [
    path('create-product/', CreateStripeProductView.as_view(), name='create-stripe-product'),
    path('create-price/', CreateStripePriceView.as_view(), name='create-stripe-price'),
    path('create-checkout-session/<int:pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
]