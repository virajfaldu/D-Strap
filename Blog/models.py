from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class category(models.Model):

    name = models.CharField(max_length=30,null=False)
    desc = models.TextField()
    img=models.ImageField(default='no found')

    def __str__(self):
	    return self.name

        
class post(models.Model):

    title =models.CharField(max_length=300,null=False)
    desc=models.TextField()
    img=models.ImageField(null=False)
    post_by = models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    views=models.IntegerField(default=0)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
	    return self.title


class comment(models.Model):

    comment = models.TextField()
    comment_by = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_to=models.ForeignKey(post,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    
    def __str__(self):
	    return self.comment

class like(models.Model):
    
    like_by = models.ForeignKey(User,on_delete=models.CASCADE)
    like_to=models.ForeignKey(post,on_delete=models.CASCADE)

    def __str__(self):
	    return f"like by {self.like_by.username} on {self.like_to.title}"