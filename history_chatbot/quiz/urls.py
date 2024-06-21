from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    path("", views.view_quizs, name="view_quizs"),
    path("<uuid:exam_id>/", views.view_quiz, name="view_quiz"),
    path("do-exam/<uuid:exam_id>/", views.do_exam, name="do_exam"),
    path("save-exam/", views.save_exam, name="save_exam"),
    path("view-result-exam/<str:username>/<uuid:exam_id>/", views.view_result_exam, name="view_result_exam"),
    path("import-quiz", views.import_quiz, name="import_quiz"),
    path("add/", views.add, name="add")
]