from rest_framework import serializers
from pi3back.core.models import Applicant, SelectionProcess, Application


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = [
            'id',
            'url',
            'about',
            'name',
            'experiences',
            'educations',
            'interests',
            'accomplishments',
            'contacts',
            'created_at',
            'updated_at'
        ]
        extra_kwargs = {
            'about': {'required': False},
            'name': {'required': False},
            'experiences': {'required': False},
            'educations': {'required': False},
            'interests': {'required': False},
            'accomplishments': {'required': False},
            'contacts': {'required': False},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }


class SelectionProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectionProcess
        fields = [
            'id',
            'description',
            'created_at',
            'ended_at',
            'is_ended',
            'category'
        ]
        read_only_fields = ['created_at', 'ended_at']


class ApplicationSerializer(serializers.ModelSerializer):
    applicant_data = ApplicantSerializer(source='applicant', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'applicant',
            'applicant_data',
            'selection_process',
            'current_step',
        ]
        read_only_fields = ['created_at', 'updated_at', 'applicant_data']
