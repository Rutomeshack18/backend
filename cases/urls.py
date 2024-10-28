from django.urls import path
from .views import CaseList
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegister
from .views import CourtListAPIView, CountyListAPIView, JudgeListAPIView

urlpatterns = [
    path('cases/', CaseList.as_view(), name='case-list'),
    path('register/', UserRegister.as_view(), name='user-register'),  
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('courts/', CourtListAPIView.as_view(), name='court-list'),
    path('counties/', CountyListAPIView.as_view(), name='county-list'),
    path('judges/', JudgeListAPIView.as_view(), name='judge-list'),
]