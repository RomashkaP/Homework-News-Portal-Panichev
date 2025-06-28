from django.db import models
from datetime import datetime
from portal.resources import POST_TYPE
from django.contrib.auth.models import User
from django.db.models import Sum

class Author (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def updating_rating(self):
        post_rating = self.post_set.aggregate(total=Sum('rating'))['total'] or 0
        total_post = post_rating * 3
        comment_rating = Comment.objects.filter(user=self.user).aggregate(total=Sum('rating'))['total'] or 0
        comment_rating_users = Comment.objects.filter(post__author=self).exclude(user=self.user)\
.aggregate(total=Sum('rating'))['total'] or 0
        self.rating = total_post + comment_rating + comment_rating_users
        self.save()

class Category (models.Model):
    name = models.CharField(max_length=100, unique=True)

class Post (models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(choices=POST_TYPE)
    time_in = models.DateTimeField(auto_now_add=True)
    categoryes = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating + 1
        self.save()
    def dislike(self):
        self.rating = self.rating - 1
        self.save()

    def preview(self):
        return f'{self.text[:124]} ...'

class PostCategory (models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment (models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = self.rating + 1
        self.save()
    def dislike(self):
        self.rating = self.rating - 1
        self.save()



