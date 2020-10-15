from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wrote')
    body = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

    
    def __str__(self):
        return f'Post #{self.id}: posted by {self.author.username} on {self.timestamp}'

class Like(models.Model):
    """
    This is the class of the likes
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "post": self.post
        }

    def __str__(self):
        return f'like #{self.id}: {self.user.username} liked {self.post}'

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('follower','followed')

    def __str__(self):
        return f'#{self.id}: {self.follower} followed {self.followed}'