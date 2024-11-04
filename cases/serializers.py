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
    
    
class CourtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Court
        fields = ['court_name']

class CaseClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseClassification
        fields = ['case_class']

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ['action_type']

class CitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citation
        fields = ['citation_text']

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = ['county_name']

class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = ['judge_name']

class CaseSerializer(serializers.ModelSerializer):
    court = CourtSerializer()
    case_classification = CaseClassificationSerializer()
    action = ActionSerializer()
    citation = CitationSerializer()
    county = CountySerializer()
    class Meta:
        model = Case
        fields = [
            'id',  
            'case_number',
            'date_delivered',
            'full_text',
            'court',
            'case_classification',
            'action',
            'citation',
            'county',  
        ]