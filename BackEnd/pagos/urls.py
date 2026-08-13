from django.urls import path
from . import views

urlpatterns = [
    path('crear-intent/', views.crear_payment_intent),
    path('webhook/', views.stripe_webhook),
]