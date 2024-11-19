from rest_framework import status
from rest_framework.generics import ListCreateAPIView
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
