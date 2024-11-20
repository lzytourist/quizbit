from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Question(models.Model):
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        db_table = 'mcq_questions'


class QuestionOption(models.Model):
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name='options'
    )
    option = models.TextField()
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.option

    class Meta:
        db_table = 'mcq_question_options'


class PracticeHistory(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='practice_history'
    ),
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name='practice_history'
    )
    attempt_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True)
    obtained_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_correct = models.BooleanField(default=False)

    # Time spent between first question view to submission
    def time_spent(self):
        if self.submitted_at is None:
            return 0
        return (self.submitted_at - self.attempt_at).total_seconds()

    class Meta:
        db_table = 'mcq_practice_histories'
