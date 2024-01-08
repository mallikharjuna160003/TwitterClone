import random
from django.http import HttpResponse,Http404,JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import render,redirect
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response 
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Tweet
from .forms import TweetForm
from .serializers import TweetCreateSerializer,TweetSerializer,TweetActionSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args,**kwargs):
    print(request.user)
    return render(request,"pages/home.html",context={"word":"Welcome"},status=200)


"""
 It is take caree of authentication checker as well!!
"""

@api_view(['POST'])
#@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request,*args,**kwargs):
    print(request)
    serializer = TweetCreateSerializer(data=request.data or None)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data,status=201)
    return Response({},status=400)



@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args,**kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data)

@api_view(['DELETE','POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args,**kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message":"You can not delete this!!"},status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message":"Tweet Deleted!!"},status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args,**kwargs):
    '''
    ID is required
    Action options are: like,unlike,retweet
    '''
    print(request.data)
    serializer = TweetActionSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({},status=404)
        obj = qs.first()
        if action=="like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data,status=200)
        elif action=="unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data,status=200)
        elif action=="retweet":
            # this todo
            parent_obj = obj
            new_tweet = Tweet.objects.create(
                user=request.user,
                parent=parent_obj,
                content=content
            )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data,status=201)
    return Response({},status=200)


@api_view(['GET'])
def tweet_list_view(request,*args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs,many=True)
    tweet_list = [x.serialize() for x in qs]
    return Response(serializer.data)


"""
Pure Django
"""
def tweet_create_view_pure_django(request,*args,**kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if not request.user.is_authenticated:
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return JsonResponse({},status=401) # unauthorized
        return redirect(settings.LOGIN_URL)
    print("ajax",request)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None # for redirecting to home 
    print("next_url",next_url)
    if form.is_valid():
        obj = form.save(commit=False)
        # Can do other form logic here!!
        obj.user = user
        obj.save()
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse(obj.serialize(),status=201)
        if next_url!=None and url_has_allowed_host_and_scheme(next_url,ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse(form.errors,status=400)

    return render(request,'components/form.html',context={'form':form})




def tweet_list_view_pure_django(request,*args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response":  tweets_list
    }
    return JsonResponse(data)




def tweet_detail_view_pure_django(request, tweet_id, *args,**kwargs):
    data = {
        "id":tweet_id
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content']=obj.content
    except:
        data["message"]="Not Found!!"
        status=404
    
    return JsonResponse(data)
