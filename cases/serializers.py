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
    court = serializers.SerializerMethodField()
    case_classification = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()
    citation = serializers.SerializerMethodField()
    county = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = [
            'id',  # Case ID
            'case_number',
            'date_delivered',
            'full_text',
            'court',               # Flattened court name
            'case_classification', # Flattened case classification
            'action',              # Flattened action type
            'citation',            # Flattened citation text
            'county',              # Flattened county name
        ]

    def get_court(self, obj):
        return obj.court.court_name if obj.court else None

    def get_case_classification(self, obj):
        return obj.case_classification.case_class if obj.case_classification else None

    def get_action(self, obj):
        return obj.action.action_type if obj.action else None

    def get_citation(self, obj):
        return obj.citation.citation_text if obj.citation else None

    def get_county(self, obj):
        return obj.county.county_name if obj.county else None