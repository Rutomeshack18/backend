from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('payments/', views.payment_init, name='create'),
    # path('success/', views.payment_success, name='success'), 
    # path('canceled/', views.payment_canceled, name='canceled'), 

]