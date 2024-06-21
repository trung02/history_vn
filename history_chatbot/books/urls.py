from django.urls import path
from . import views


app_name = "books"

urlpatterns = [
    path("", views.import_data, name="import_data"),
    path("segment/", views.word_segmented, name="woed_segment"),
    path("embeddings/", views.embeddings,name="embeddings"),
    path("search/", views.search, name="search"),
    path("add/", views.add, name="add")
]