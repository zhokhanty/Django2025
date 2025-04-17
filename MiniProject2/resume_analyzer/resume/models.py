from django.db import models
from django.contrib.auth import get_user_model
from pydantic import BaseModel, EmailStr
from typing import List
from marshmallow import Schema, fields

class ResumeSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    skills = fields.List(fields.Str())

class ParsedResume(BaseModel):
    name: str
    email: EmailStr
    skills: List[str]
    experience_years: float

User = get_user_model()

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    parsed_data = models.JSONField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    skills = models.JSONField(default=list)

class JobPosting(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    min_experience = models.IntegerField(default=0)
    location = models.CharField(max_length=100)

class ResumeFeedback(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='feedback')
    created_at = models.DateTimeField(auto_now_add=True)
    skill_gaps = models.JSONField(default=list)               
    formatting_suggestions = models.JSONField(default=list)
    keyword_recommendations = models.JSONField(default=list)