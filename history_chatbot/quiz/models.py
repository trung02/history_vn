from django.db import models
import uuid
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
    choise_1 = models.CharField(max_length=200)
    choise_2 = models.CharField(max_length=200)
    choise_3 = models.CharField(max_length=200)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'exam'], name='unique_question_exam')
        ]

    def __str__(self):
        return self.question