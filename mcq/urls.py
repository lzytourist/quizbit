from django.urls import path

from .views import MCQListCreateAPIView

urlpatterns = [
    path('questions/', MCQListCreateAPIView.as_view(), name='questions'),
]
