from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.


# custom models manager
class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "DRAFT"
        PUBLISHED = "PB", "PUBLISHED"
    
    


    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        # by using this now for sluf models has to save unique publish date
        # check only date not time in publish
        unique_for_date="publish",
    )

    # on_delete not sepecified to Django
    # it is an SQL standard

    # related_name to specify the name of the reverse relationship

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    # the default manager
    objects = models.Manager()
    # our custom manager
    published = PublishManager()

    tags = TaggableManager()

    class Meta:
        ordering = ["publish"]

        # NOTE
        # index will increase the performance for query filtering results by field
        # index ordering is not spported by MySQL it will created as a normal index for the database

        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title

    # build the url dynamically using the url name

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )
    

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default= True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields = ['created'])
        ]

    def __str__(self):
        return f"Comment y {self.name} on {self.post}"
