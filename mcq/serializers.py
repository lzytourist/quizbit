from rest_framework import serializers

from .models import Question, QuestionOption, PracticeHistory


class QuestionOptionSerializer(serializers.ModelSerializer):
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


class PracticeHistorySerializer(serializers.ModelSerializer):
    time_spent = serializers.SerializerMethodField(source='get_time_spent')

    class Meta:
        model = PracticeHistory
        fields = '__all__'

    def get_time_spent(self, obj):
        return obj.time_spent()


class SubmissionSerializer(serializers.Serializer):
    options = serializers.JSONField(required=True)
    question = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(),
        required=True
    )

    def validate(self, attrs):
        options = attrs.get('options')
        if type(options) is not list:
            raise serializers.ValidationError({
                'options': ['Must contain list of options']
            })
        return attrs
