from django.db import models
import uuid
from django.contrib import admin
# Create your models here.
class Grade(models.Model):
    id = models.UUIDField(default=uuid.uuid1, primary_key=True)
    name = models.CharField(max_length=500, unique=True)
    image = models.ImageField(upload_to='image_book/', default='')
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


class AuthorAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"


import json
from django.core.exceptions import ValidationError
def validate_json(value):
    try:
        data = json.loads(value.read().decode('utf-8'))
    except ValueError as e:
        raise ValidationError("Invalid JSON file")

class JsonBook(models.Model):
    image = models.ImageField(upload_to='image_book/', default='image_book/Lich-su-12.jpg')
    json_file = models.FileField(upload_to='json_files/', validators=[validate_json])
    def __str__(self):
        return f"dir: {self.json_file.url}"
