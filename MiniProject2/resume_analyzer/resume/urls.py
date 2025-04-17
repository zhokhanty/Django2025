from django.urls import path
from .views import (
    ResumeUploadView, MatchCandidatesView, CreateJobPostingView, GenerateFeedbackView
)

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='upload-resume'),
    path('match/<int:job_id>/', MatchCandidatesView.as_view(), name='match-candidates'),
    path('job/create/', CreateJobPostingView.as_view(), name='create-job'),
    path('resume/<int:resume_id>/feedback/<int:job_id>/', GenerateFeedbackView.as_view(), name='generate-feedback')
]