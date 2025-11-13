from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse 
from django.utils.text import slugify

# access the user model
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    # Meta class to set the plural name of the model
    class Meta:
        verbose_name_plural = "Categories"

    # Method to return the name of the category
    def __str__(self):
        return self.name

class Post(models.Model):
    # STATUS_CHOICES is a tuple of tuples to set the choices for the status field
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title
    
    # Method to return the absolute URL of the post
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    # Method to save the post
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering =["created_at"]
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

