from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions

from .models import Article
from .serializers import ArticleSerializer
from .services import fetch_articles_from_api

class UpdateArticlesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cache_key = "articles_update"
        if cache.get(cache_key):
            return Response({"detail": "Данные недавно обновлены, подождите 30 минут"}, status=400)

        articles_data = fetch_articles_from_api()
        new_articles = []

        for item in articles_data:
            obj, created = Article.objects.get_or_create(
                url=item["url"],
                defaults={
                    "source_id": item["source"].get("id") if item.get("source") else None,
                    "source_name": item["source"].get("name") if item.get("source") else "",
                    "author": item.get("author"),
                    "title": item.get("title"),
                    "description": item.get("description"),
                    "url_to_image": item.get("urlToImage"),
                    "published_at": item.get("publishedAt"),
                    "content": item.get("content"),
                },
            )
            if created:
                new_articles.append(obj)

        cache.set(cache_key, True, 60 * 30)  # 30 минут
        return Response({"added": len(new_articles)}, status=200)


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all().order_by("-published_at")

    def get_queryset(self):
        qs = super().get_queryset()

        # Фильтр свежих новостей (24 часа)
        fresh = self.request.query_params.get("fresh")
        if fresh == "true":
            since = timezone.now() - timedelta(hours=24)
            qs = qs.filter(published_at__gte=since)

        # Фильтр по заголовку
        title_contains = self.request.query_params.get("title_contains")
        if title_contains:
            qs = qs.filter(title__icontains=title_contains)

        return qs

    def list(self, request, *args, **kwargs):
        cache_key = f"articles_list:{request.get_full_path()}"
        cached_response = cache.get(cache_key)
        if cached_response:
            return Response(cached_response)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60 * 10)  # 10 минут
        return response
