from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Tweet
# Create your tests here.

User = get_user_model()
class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cfe",password="somepassword")
        #User.objects.create_user(username="cfe1",password="somepassword")
        tweet_object = Tweet.objects.create(content="my tweet",
            user=self.user)
        tweet_object = Tweet.objects.create(content="my tweet",
            user=self.user)
        tweet_object = Tweet.objects.create(content="my tweet",
            user=self.user)
        self.current_count = Tweet.objects.all().count()
    
    def test_user_exists(self):
        self.assertEqual(self.user.username,"cfe")

    def test_tweet_created(self):
        tweet_object = Tweet.objects.create(content="my tweet",
            user=self.user)
        self.assertEqual(self.user.username,"cfe") 
        self.assertEqual(tweet_object.id,4)
    
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        print(response.json())
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),3)
    
    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
            {"id":2,"action":"like"})
        self.assertEqual(response.status_code,200)
        response = client.post("/api/tweets/action/",
            {"id":2,"action":"unlike"})
        self.assertEqual(response.status_code,200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count,0)
        # self.assertEqual(len(response.json()),3)
    def test_action_retweet(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",
            {"id":2,"action":"retweet"})
        self.assertEqual(response.status_code,201)
        data = response.json()
        new_tweet_id = data.get("id")
        self.assertNotEqual(2,new_tweet_id)
        self.assertEqual(self.current_count+1, new_tweet_id)
    
    def test_tweet_create_api_view(self):
        data = {"content":"This is my test tweet"}
        client = self.get_client()
        response = client.post("/api/tweets/create/",data)
        self.assertEqual(response.status_code,201)
        data = response.json()
        new_tweet_id = data.get("id")
        self.assertEqual(self.current_count+1, new_tweet_id)
    
    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEqual(response.status_code,200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id,1)
    
    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code,200)
     


    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username,password="somepassword")
        #self.assertEqual(client.username,self.user.username)
        return client

     
     
        

