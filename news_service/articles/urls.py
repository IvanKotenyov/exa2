from django.urls import path
from .views import UpdateArticlesView, ArticleListView

urlpatterns = [
    path("update/", UpdateArticlesView.as_view(), name="articles-update"),
    path("", ArticleListView.as_view(), name="articles-list"),
]
