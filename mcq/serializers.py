from rest_framework import serializers

from .models import Question, QuestionOption


class QuestionOptionSerializer(serializers.ModelSerializer):
    # def validate(self, attrs):
    #     question_id = attrs.get('question')
    #
    #     # Validate if question exists in the database
    #     if not Question.objects.filter(pk=question_id).exists():
    #         raise serializers.ValidationError({
    #             'question': ['Question does not exist']
    #         })
    #
    #     return attrs

    class Meta:
        model = QuestionOption
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
