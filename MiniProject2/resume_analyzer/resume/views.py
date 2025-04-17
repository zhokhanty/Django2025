from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Resume, JobPosting, ResumeFeedback
from .serializers import ResumeUploadSerializer, JobPostingSerializer, ResumeFeedbackSerializer, ResumeModelSerializer
from .utils import parse_resume
from sentence_transformers import SentenceTransformer, util
from rest_framework.views import APIView
from .utils import compute_skill_gaps, formatting_suggestions, keyword_recommendations
from rest_framework import viewsets

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeModelSerializer

model = SentenceTransformer('all-MiniLM-L6-v2')

class ResumeUploadView(generics.CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeUploadSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        resume = serializer.save(user=self.request.user)
        file = self.request.FILES['file']
        parsed_data = parse_resume(file)
        resume.parsed_data = parsed_data
        resume.save()

def rate_resume_against_job(resume_text, job_description):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    vectorizer = TfidfVectorizer().fit_transform([resume_text, job_description])
    score = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]
    return round(score * 100, 2)

def calculate_similarity(text1, text2):
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    return util.cos_sim(emb1, emb2).item()

def score_resume_to_job(resume, job):
    similarity = calculate_similarity(resume.parsed_text, job.description)

    skills_match = len(set(resume.skills) & set(job.required_skills)) / len(job.required_skills or [1])
    experience_score = 1 if resume.experience_years >= job.min_experience else 0
    location_score = 1 if resume.location.lower() == job.location.lower() else 0

    final_score = 0.6 * similarity + 0.2 * skills_match + 0.1 * experience_score + 0.1 * location_score
    return round(final_score, 2)

class MatchCandidatesView(APIView):
    def get(self, request, job_id):
        job = JobPosting.objects.get(id=job_id)
        resumes = Resume.objects.all()

        results = []
        for resume in resumes:
            score = score_resume_to_job(resume, job)
            results.append({
                "user": resume.user.username,
                "score": score,
                "skills": resume.skills,
                "experience": resume.experience_years,
                "location": resume.location
            })

        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        return Response(sorted_results)

class CreateJobPostingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JobPostingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(recruiter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenerateFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id, job_id):
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        job    = get_object_or_404(JobPosting, id=job_id)

        text = resume.parsed_data.get('text', '')
        gaps = compute_skill_gaps(resume.skills)
        fmt  = formatting_suggestions(text)
        kws  = keyword_recommendations(text, job)

        feedback, _ = ResumeFeedback.objects.update_or_create(
            resume=resume,
            defaults={
                'skill_gaps': gaps,
                'formatting_suggestions': fmt,
                'keyword_recommendations': kws,
            }
        )
        serializer = ResumeFeedbackSerializer(feedback)
        return Response(serializer.data, status=201)