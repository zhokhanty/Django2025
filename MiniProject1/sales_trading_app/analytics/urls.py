from django.urls import path
from .views import AnalyticsReportListView, AnalyticsReportDetailView

urlpatterns = [
    path('reports/', AnalyticsReportListView.as_view(), name='analytics-report-list'),
    path('reports/<int:pk>/', AnalyticsReportDetailView.as_view(), name='analytics-report-detail'),
]