from rest_framework import serializers
from typing import TypedDict
from django.contrib.auth import get_user_model

User = get_user_model()

from pi3back.occurrences.models import (
    Occurrence,
    Classroom
)

class StudentSerializer(serializers.ModelSerializer):
    occurrence_count = serializers.SerializerMethodField()

    def get_occurrence_count(self, obj) -> int:
        return obj.student_occurrences.count()

    class Meta:
        model = User
        fields = ['id', 'nome', 'occurrence_count']

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'nome']

class OccurrenceSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(read_only=True)

    class Meta:
        model = Occurrence
        exclude = ['created_by']

    def to_internal_value(self, data):
        data = super().to_internal_value(data)     
        data['created_by'] = self.context['request'].user
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['students'] = StudentSerializer(instance.student).data
        if data.get('created_by', None):
            data['teachers'] = TeacherSerializer(instance.created_by).data
            del data['created_by']
        return data

class ClassroomSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, read_only=True)
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['teachers'] = TeacherSerializer(instance.members.filter(is_professor=True), many=True).data
        representation['students'] = StudentSerializer(instance.members.filter(is_aluno=True), many=True).data
        return representation
    