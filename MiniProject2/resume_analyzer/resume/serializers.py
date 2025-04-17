from rest_framework import serializers
from .models import ParsedResume, JobPosting, ResumeFeedback

class ResumeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParsedResume
        fields = '__all__'

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParsedResume
        fields = ['id', 'file', 'uploaded_at', 'parsed_data', 'score']
        read_only_fields = ['parsed_data', 'score', 'uploaded_at']

class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = '__all__'
        read_only_fields = ['recruiter']

class ResumeFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeFeedback
        fields = '__all__'