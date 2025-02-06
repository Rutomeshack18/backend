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
from rest_framework.pagination import CursorPagination
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import AzureOpenAI
logger = logging.getLogger(__name__)
from django.conf import settings
from .users import UpdateUserDetails, DeleteUserAccount
from .serializers import UserSerializer


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

# class CaseCursorPagination(CursorPagination):
#     page_size = 20
#     ordering = '-id'

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
    # pagination_class = CaseCursorPagination

    
class CaseDetail(generics.RetrieveAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseDetailSerializer
    lookup_field = 'id'

client = AzureOpenAI(
  azure_endpoint = settings.AZURE_ENDPOINT,
  api_key=settings.AZURE_API_KEY,  
  api_version=settings.API_VERSION
)

@csrf_exempt
def summarize_case(request, case_number):
    case = get_object_or_404(Case, case_number=case_number)

    # Construct the summarization instructions
    input_text = (
        "Summarize the case text with the following details in 200-300 words: "
        "1. Case type. "
        "2. Case number. "
        "3. Parties involved. "
        "4. The court in which the case was adjudicated or is ongoing. "
        "5. A brief description of the case. "
        "6. Any decisions made, if a ruling has been given.\n\n"
        f"Case Text:\n{case.full_text}"
    )

    # Construct the prompt for Azure OpenAI
    conversation = [
        {
            "role": "system",
            "content": "You are a legal assistant specializing in summarizing case texts. "
                       "Follow the provided instructions and ensure the summary is concise."
        },
        {"role": "user", "content": input_text}
    ]

    try:
        # Call Azure OpenAI
        response = client.chat.completions.create(
            model=settings.DEPLOYMENT_NAME,  # Model deployment name
            messages=conversation,
            max_tokens=300,  # Adjust based on desired summary length
            temperature=0.5,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the assistant's summary
        if response.choices:
            summary = response.choices[0].message.content
            return JsonResponse({"case_number": case.case_number, "summary": summary})
        else:
            return JsonResponse({"error": "No response from AI model."}, status=500)

    except Exception as e:
        logger.error(f"Error summarizing case: {str(e)}")
        return JsonResponse({"error": f"Internal error: {str(e)}"}, status=500)
