from django.urls import path
from . import views


app_name = "books"

urlpatterns = [
    path("", views.import_data, name="import_data"),
]