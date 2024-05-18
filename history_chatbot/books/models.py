from django.db import models
import uuid
# Create your models here.
class Grade(models.Model):
    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    id = models.UUIDField(default=uuid.uuid1,primary_key=True)
    name = models.CharField(max_length=500)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    id = models.UUIDField(default=uuid.uuid1,primary_key=True)
    name = models.CharField(max_length=500)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Title(models.Model):
    id = models.UUIDField(default=uuid.uuid1,primary_key=True)
    name = models.CharField(max_length=500)
    content = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

