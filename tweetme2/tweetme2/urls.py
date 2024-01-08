from django.contrib import admin
from django.urls import path,include
# from tweets import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tweets/', include("tweets.urls")),
]
