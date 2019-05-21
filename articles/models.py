from django.db import models

class Article(models.Model):
    FORMAT_CHOICES = [('news', 'news'), ('faq', 'faq'), ('longread', 'longread')]
    ITER_KEYS = ['id', 'slug', 'format', 'title']

    slug = models.CharField(max_length=120, db_index=True)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, db_index=True)
    title = models.CharField(max_length=120)
    create_date = models.DateTimeField(auto_now_add=True, editable=False)
    text = models.TextField(blank=True)

    def __str__(self):
        return f"{self.format}/{self.slug}"

    def __iter__(self):
        for k in self.ITER_KEYS:
            yield k, object.__getattribute__(self, k)
