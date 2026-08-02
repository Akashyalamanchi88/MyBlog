from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


    title = models.CharField(
        max_length=200,
        blank=True
    )


    image = models.ImageField(
        upload_to="blog_images/",
        blank=True,
        null=True
    )


    content = CKEditor5Field(
        'Content',
        config_name='extends',
        blank=True
    )


    likes = models.ManyToManyField(
        User,
        related_name="liked_posts",
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):

        return self.title if self.title else "Untitled Post"
class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="like_objects"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"