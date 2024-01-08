from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tweets.views import (
    tweet_detail_view,
    tweet_list_view,
    tweet_create_view,
    tweet_delete_view,
    tweet_action_view,
)
'''
CLIENT
Base ENDPOINT /api/tweets/
'''
urlpatterns = [
   
    path("",tweet_list_view),
    path("action/",tweet_action_view),
    path("create/",tweet_create_view),    
    path("<int:tweet_id>/",tweet_detail_view),
    path("<int:tweet_id>/delete/",tweet_delete_view),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)