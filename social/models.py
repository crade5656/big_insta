from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)


    def __str__(self):
        return f"Profile({self.user.username})"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f"Post#{self.pk} by {self.author.username}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_at']


    def __str__(self):
        return f"Comment#{self.pk} by {self.author.username}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'post')


    def __str__(self):
        return f"Like {self.user.username} -> Post#{self.post_id}"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('follower', 'following')


    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"