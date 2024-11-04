from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics, filters as drf_filters  # Importing SearchFilter here
from .models import Case
from .serializers import CaseSerializer
from .serializers import UserSerializer
from .models import CustomUser


def home(request):
    return render(request, 'base.html')

class UserRegister(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class CaseFilter(filters.FilterSet):
    case_number = filters.CharFilter(lookup_expr='icontains')
    date_delivered = filters.DateFilter()
    court = filters.CharFilter(field_name='court__court_name', lookup_expr='icontains')
    county = filters.CharFilter(field_name='county__county_name', lookup_expr='icontains')

    class Meta:
        model = Case
        fields = ['case_number', 'date_delivered', 'court', 'county']

class CaseList(generics.ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    filter_backends = (filters.DjangoFilterBackend, drf_filters.SearchFilter)
    filterset_class = CaseFilter
    search_fields = ['case_number', 'full_text']