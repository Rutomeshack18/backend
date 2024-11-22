from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics, filters as drf_filters  # Importing SearchFilter here
from .models import Case
from .serializers import CaseSerializer, CaseDetailSerializer
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import requests
from django.conf import settings 
from django_filters.rest_framework import DjangoFilterBackend

def home(request):
    return render(request, 'base.html')

class UserRegister(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class CaseFilter(filters.FilterSet):
    case_number = filters.CharFilter(lookup_expr='icontains')  # Searching with case_number
    date_delivered = filters.DateFilter()
    court = filters.CharFilter(field_name='court__court_name', lookup_expr='icontains')
    county = filters.CharFilter(field_name='county__county_name', lookup_expr='icontains')

    class Meta:
        model = Case
        fields = ['case_number', 'date_delivered', 'court', 'county']

class CaseList(generics.ListAPIView):
    queryset = Case.objects.select_related(
        'court', 'case_classification', 'action', 'citation', 'county'
    ).only(
        'id', 'case_number', 'date_delivered', 
        'court__court_name', 'case_classification__case_class', 
        'action__action_type', 'citation__citation_text', 'county__county_name'
    )  # Use select_related and only to reduce query size
    serializer_class = CaseSerializer
    filter_backends = (DjangoFilterBackend, drf_filters.SearchFilter)
    filterset_class = CaseFilter
    search_fields = ['case_number', 'full_text']

class CaseDetail(generics.RetrieveAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseDetailSerializer
    lookup_field = 'id'

@api_view(['GET'])
def summarize_case(request, case_number):
    # Fetch the case by its case_number
    case = get_object_or_404(Case, case_number=case_number)

    # Prepare full text for summarization
    full_text = case.full_text

    # Add summarization instructions with word count
    instructions = (
        "Summarize the case text with the following details in 200-300 words: "
        "1. Case type. "
        "2. Case number. "
        "3. Parties involved. "
        "4. The court in which the case was adjudicated or is ongoing. "
        "5. A brief description of the case. "
        "6. Any decisions made, if a ruling has been given."
    )
    input_text = f"{instructions}\n\n{full_text}"

    # Hugging Face API URL and headers
    api_url = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"
    }

    # Post request to Hugging Face API
    try:
        response = requests.post(api_url, headers=headers, json={"inputs": input_text})
        response.raise_for_status()  # Raise HTTPError for bad responses
        response_data = response.json()
        summary = response_data[0].get('summary_text', "No summary available")
    except requests.exceptions.RequestException as e:
        return Response({"error": "Failed to summarize the text", "details": str(e)}, status=500)
    except (KeyError, IndexError):
        return Response({"error": "Unexpected response from summarization API"}, status=500)

    # Return the structured response
    return Response({
        "case_number": case.case_number,
        "summary": summary
    })