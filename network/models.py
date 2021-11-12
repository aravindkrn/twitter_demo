from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils.models import TimeStampedModel


class User(AbstractUser):
    follower = models.ManyToManyField("self", related_name="follower_users")
    following = models.ManyToManyField("self", related_name="following_users")

    def name(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name or self.username


class Post(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        short_content = self.content
        if len(short_content) > 10:
            short_content = f"{short_content[:10]}..."
        return f"{self.author} [{short_content}]"
