from django.urls import path
from .views import chatbot_view, legal_doc_generator_view

urlpatterns = [
    path('api/chatbot/', chatbot_view, name='chatbot_response'),
    path('api/legal-doc-generator/', legal_doc_generator_view, name='legal_doc_generator'),
]