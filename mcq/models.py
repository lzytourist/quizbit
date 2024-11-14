from django.db import models


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
