from django.db.models import Q
from django.utils import timezone

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Question, QuestionOption
from .serializers import QuestionSerializer, QuestionOptionSerializer


class MCQListCreateAPIView(ListCreateAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Check if options are provided
        # Create question options
        options = request.data.get('options')
        if options is not None:
            options_data = []
            for option in options:
                options_data.append({
                    'option': option.get('option'),
                    'is_correct': True if option.get('is_correct') and option.get('is_correct') == True else False,
                    'question': serializer.data.get('id'),
                })

            # Check if options are valid
            option_serializer = QuestionOptionSerializer(data=options_data, many=True)
            option_serializer.is_valid(raise_exception=True)

            # Option list for bulk create
            option_list = []
            for option in option_serializer.data:
                option_list.append(QuestionOption(
                    option=option.get('option'),
                    is_correct=option.get('is_correct'),
                    question_id=option.get('question')
                ))
            QuestionOption.objects.bulk_create(option_list)

        return Response(
            data={
                **serializer.data,
                'options': QuestionOptionSerializer(
                    QuestionOption.objects.filter(question=serializer.data['id']),
                    many=True
                ).data
            },
            status=status.HTTP_201_CREATED
        )


class MCQRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return super().get_permissions()

    # Store attempt time for a user
    def get_object(self):
        question = super().get_object()
        if self.request.method == 'GET' and not self.request.user.is_staff:
            last_history = question.practice_history.filter(
                Q(user=self.request.user) &
                Q(submitted_at__isnull=True)
            ).first()

            if last_history is None:
                question.practice_history.create(
                    user=self.request.user,
                )
        return question


class OptionListCreateAPIView(ListCreateAPIView):
    serializer_class = QuestionOptionSerializer
    queryset = QuestionOption.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = PageNumberPagination


class OptionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionOptionSerializer
    queryset = QuestionOption.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
