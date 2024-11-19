from django.urls import path

from .views import MCQListCreateAPIView, MCQRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('questions/', MCQListCreateAPIView.as_view(), name='questions'),
    path('questions/<int:pk>/', MCQRetrieveUpdateDestroyAPIView.as_view(), name='question'),
]
