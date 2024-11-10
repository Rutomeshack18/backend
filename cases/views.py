from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics, filters as drf_filters  # Importing SearchFilter here
from .models import Case
from .serializers import CaseSerializer
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import requests


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

@api_view(['GET'])
def summarize_case(request, case_number):
    # Fetch the case by its case_number
    case = get_object_or_404(Case, case_number=case_number)
    
    full_text = case.full_text
    
    # Hugging Face API URL and headers
    api_url = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
    headers = {
        "Authorization": "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" 
    }
    
    response = requests.post(api_url, headers=headers, json={"inputs": full_text})
    

    if response.status_code == 200:
        summary = response.json()[0]['summary_text']
    else:
        return Response({"error": "Failed to summarize the text"}, status=response.status_code)


    serializer = CaseSerializer(case)
    
    return Response({
        "case_number": case.case_number,
        "summary": summary,
        "case_data": serializer.data
    })

