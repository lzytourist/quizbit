from django.urls import path

from .views import MCQListCreateAPIView, MCQRetrieveUpdateDestroyAPIView, \
    OptionListCreateAPIView, OptionRetrieveUpdateDestroyAPIView, \
    PracticeHistoryListAPIView

urlpatterns = [
    path('questions/', MCQListCreateAPIView.as_view(), name='questions'),
    path('questions/<int:pk>/', MCQRetrieveUpdateDestroyAPIView.as_view(), name='question'),
    path('options/', OptionListCreateAPIView.as_view(), name='options'),
    path('options/<int:pk>/', OptionRetrieveUpdateDestroyAPIView.as_view(), name='option'),
    path('practice-history/', PracticeHistoryListAPIView.as_view(), name='practice-history'),
]
