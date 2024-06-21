from django.db import models
from django.contrib.auth.models import User
import uuid
import json
from django.core.exceptions import ValidationError
# Create your models here.
class Exam(models.Model):
    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=200)
    choice_1 = models.CharField(max_length=200)
    choice_2 = models.CharField(max_length=200)
    choice_3 = models.CharField(max_length=200)
    choice_4 = models.CharField(max_length=200)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'exam'], name='unique_question_exam')
        ]

    def __str__(self):
        return self.question

class DoExam(models.Model):
    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'exam', 'question'], name='unique_user_exam_question')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.exam.name} - {self.question.question}"


def validate_json(value):
    try:
        data = json.loads(value.read().decode('utf-8'))
    except ValueError as e:
        raise ValidationError("Invalid JSON file") 
class ExamJson(models.Model):
    json_file = models.FileField(upload_to='exam/', validators=[validate_json], default='')
    def __str__(self):
        return f"dir: {self.json_file.url}"





