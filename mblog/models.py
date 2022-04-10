from django.utils import timezone
from django.db import models
from django.urls import reverse  #try to work reverse in model
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approve_comment=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('mblog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100) #comment kiểu nặc danh tự ghi tên rồi cmd
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    approve_comment = models.BooleanField(default=False)

    def approve(self):
        self.approve_comment = True
        self.save()
        
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.approve_comment