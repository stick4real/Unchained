from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=500, default='')
    date = models.DateTimeField('date published')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    date = models.DateTimeField('date published')