from django.urls import path
from .views import initialize_payment

urlpatterns = [
    path('payments/', initialize_payment, name='initialize-payment'),
]