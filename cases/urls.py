from django.urls import path, include
from .views import CaseList, CaseDetail
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegister
from . import views


urlpatterns = [
    path('cases/', CaseList.as_view(), name='case-list'),  # List of cases
    path('cases/<int:id>/', CaseDetail.as_view(), name='case-detail'),
    path('register/', UserRegister.as_view(), name='user-register'),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),  
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('summarize/<str:case_number>/', views.summarize_case, name='summarize_case'),
]