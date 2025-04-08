from rest_framework import serializers
from pi3back.core.models.linkedin_profile import LinkedInProfile


class LinkedInProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedInProfile
        fields = [
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
