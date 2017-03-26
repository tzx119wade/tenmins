from django.db import models
from django.utils import timezone
from faker import Faker
import re

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=500)
    img = models.CharField(max_length=250)
    content = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    createtime = models.DateField(default=timezone.now)
    editor_choice = models.BooleanField(default=False)
    CATE_CHOICE = {
        ('best','best'),
        ('hot','hot'),
    }

    cate_choice = models.CharField(choices=CATE_CHOICE,max_length=10,blank=True,null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(null=True,blank=True,max_length=50)
    avatar = models.URLField(default='images/default.png')
    content = models.TextField(null=True,blank=True)
    createtime = models.DateTimeField(default=timezone.now)
    belong_to = models.ForeignKey(to=Article,related_name='comments',blank=True,null=True)

    def __str__(self):
        return self.name
