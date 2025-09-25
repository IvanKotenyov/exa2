from django.db import models
from django.conf import settings
from articles.models import Article

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "article")

    def __str__(self):
        return f"{self.user.email} -> {self.article.title}"
