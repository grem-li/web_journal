from django.db import models

class Article(models.Model):
    slug = models.CharField(max_length=120, db_index=True)
    format = models.CharField(max_length=10, db_index=True)
    title = models.CharField(max_length=120)
    create_date = models.DateTimeField(auto_now_add=True, editable=False)
    text = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title}"

    def __unicode__(self):
        return f"{self.format}/{self.slug}"

