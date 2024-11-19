from rest_framework import serializers

from .models import Question, QuestionOption


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


class QuestionOptionSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        question_id = attrs.get('question_id')

        # Validate if question exists in the database
        if not Question.objects.filter(pk=question_id).exists():
            raise serializers.ValidationError({
                'question_id': ['Question does not exist']
            })

        return attrs

    class Meta:
        model = QuestionOption
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
