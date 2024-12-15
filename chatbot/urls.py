from django.urls import path
from .views import chatbot_view

urlpatterns = [
    path('api/chatbot/', chatbot_view, name='chatbot_response'),
]