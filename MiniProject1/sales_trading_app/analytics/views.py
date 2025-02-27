from rest_framework import generics
from .models import AnalyticsReport
from .serializers import AnalyticsReportSerializer

class AnalyticsReportListView(generics.ListCreateAPIView):
    queryset = AnalyticsReport.objects.all()
    serializer_class = AnalyticsReportSerializer

class AnalyticsReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AnalyticsReport.objects.all()
    serializer_class = AnalyticsReportSerializer