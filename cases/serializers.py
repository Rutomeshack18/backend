from rest_framework import serializers
from .models import Case, Court, CaseClassification, County, Action, Citation, Judge, Party
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class CaseSerializer(serializers.ModelSerializer):
    court = serializers.CharField(source='court.court_name')
    case_classification = serializers.CharField(source='case_classification.case_class')
    action = serializers.CharField(source='action.action_type')
    citation = serializers.CharField(source='citation.citation_text')
    county = serializers.CharField(source='county.county_name')

    class Meta:
        model = Case
        fields = [
            'id',  # Case ID
            'case_number',
            'date_delivered',
            'court',
            'case_classification',
            'action',
            'citation',
            'county',
        ]


class CaseDetailSerializer(serializers.ModelSerializer):
    case_number = serializers.CharField()  
    full_text = serializers.CharField()   

    class Meta:
        model = Case
        fields = ['case_number', 'full_text']