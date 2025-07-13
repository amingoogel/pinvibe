from django.db import models
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Pin(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='pins/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pins')
    board = models.ForeignKey('boards.Board', on_delete=models.SET_NULL, null=True, blank=True, related_name='pins')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_pins', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pin', 'user')
