from django.db import models

class Article(models.Model):
    source_id = models.CharField(max_length=255, null=True, blank=True)
    source_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)
    url_to_image = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField()
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
