from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=250)
    abstract = models.TextField()
    date = models.DateField()
    authors = models.CharField(max_length=300)
    body = models.TextField()
    bibliography = models.TextField()

    def __str__(self):
        return self.title
