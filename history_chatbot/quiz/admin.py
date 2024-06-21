# admin.py
import json
from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from .models import *
import requests

# Register your models here.
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(DoExam)

class ExamJsonAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Thực hiện logic tùy chỉnh trước khi lưu
        if obj.json_file:
            obj.json_file.seek(0)  # Đặt lại con trỏ tệp về đầu
            try:
                data = json.loads(obj.json_file.read().decode('utf-8'))
                response = requests.post('http://127.0.0.1:8000/quiz/add/', json=data)
                if response.status_code == 200:  # Thay 200 bằng mã trạng thái phù hợp
                    messages.success(request, "Nội dung sách đã tự động cập nhật vào database")
                else:
                    print(f"Lỗi: {response.status_code}")
                    messages.error(request, "Nội dung sách đã tồn tại! Vui lòng kiểm tra lại.")
            except json.JSONDecodeError:
                print("Tệp JSON không hợp lệ")
            finally:
                obj.json_file.seek(0)  # Đặt lại con trỏ tệp về đầu để chuẩn bị lưu
            super().save_model(request, obj, form, change)

admin.site.register(ExamJson, ExamJsonAdmin)

