from django.db import models
from django.conf import settings
import random

User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # string Tweet is used bcz it is below the class
    tweet = models.ForeignKey("Tweet",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)




# Create your models here.
class Tweet(models.Model):

    # id = models.AutoField(primary_key=True)
    parent = models.ForeignKey("self",null=True,on_delete=models.SET_NULL)
    user = models.ForeignKey(User,on_delete=models.CASCADE) # many users can have many tweets
    likes = models.ManyToManyField(User,related_name="tweet_user",blank=True,through=TweetLike) # one like can have many users
    content = models.TextField(blank=True,null=True)
    image = models.FileField(upload_to="images/",blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-id']
    
    # def __str__(self):
    #     return self.content
    
    @property
    def is_retweet(self):
        return self.parent!=None

    def serialize(self):
        '''
        this can be no need but in pure django it required
        '''
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0,200)
        }