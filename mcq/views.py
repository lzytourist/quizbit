from django.db.models import Q
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Question, QuestionOption, PracticeHistory
from .serializers import QuestionSerializer, QuestionOptionSerializer, PracticeHistorySerializer, SubmissionSerializer


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


class PracticeHistoryListAPIView(ListAPIView):
    queryset = PracticeHistory.objects.all()
    serializer_class = PracticeHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get only current user practice history if user is not admin
        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user).order_by('-id')

        # Filter specific user practice history
        # Only if authenticated user is admin
        elif self.request.query_params.get('user'):
            return queryset.filter(user=self.request.query_params.get('user'))

        return queryset


class SubmissionAPIView(APIView):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        attempt_history = self.request.user.practice_history.filter(
            Q(question_id=serializer.data.get('question')) &
            Q(submitted_at__isnull=True)
        ).first()
        if attempt_history is None:
            # Check if previously attempted with wrong answer
            # Take the first attempt
            attempt_history = self.request.user.practice_history.filter(
                question_id=serializer.data.get('question')
            ).order_by('id').first()

            if attempt_history is None:
                # Illegal access, without accessing the question first
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Create new record having first attempt time
            # Occurs when user is submitting again for the same question without accessing the question again
            attempt_history = self.request.user.practice_history.create(
                attempt_at=attempt_history.attempt_at,
                question_id=serializer.data.get('question'),
            )

        attempt_history.submitted_at = timezone.now()

        answers = attempt_history.question.options.filter(is_correct=True).values('id')
        answer_ids = set([answer['id'] for answer in answers])
        given_answers = set(serializer.data.get('options', []))

        correct = answer_ids.intersection(given_answers)
        if answer_ids == given_answers:
            attempt_history.is_correct = True

        attempt_history.obtained_marks = max(
            0.0,
            (len(correct) - 0.25 * (len(given_answers) - len(correct))) / len(answer_ids)
        )
        attempt_history.save()

        return Response(data={
            **PracticeHistorySerializer(attempt_history).data
        }, status=status.HTTP_201_CREATED)
