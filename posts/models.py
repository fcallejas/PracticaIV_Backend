from django.contrib.auth.models import User
from django.db import models

VISIBILITY_PUBLIC = 'PUB'
VISIBILITY_PRIVATE = 'PRI'

VISIBILITY = (
    (VISIBILITY_PUBLIC, 'Público'),
    (VISIBILITY_PRIVATE, 'Privado')
)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=150)
    intro = models.TextField(max_length=300, null=True, blank=True)
    body = models.TextField()
    media_url = models.URLField(null=True, blank=True)
    category = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User)
    visibility = models.CharField(max_length=3, choices=VISIBILITY, default=VISIBILITY_PUBLIC)
    publicate_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
