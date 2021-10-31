from django.urls import path

from tweets.api.v1.views import (
    TagListAPIView,
    TweetListCreateAPIView,
    TweetRetrieveUpdateDestroyAPIView
)

app_name = 'tweets-api-v1'

urlpatterns = [
    path('tags/', TagListAPIView.as_view(), name='tag_list'),
    path('tweets/', TweetListCreateAPIView.as_view(), name='tweet_list_create'),
    path('tweets/<int:pk>/', TweetRetrieveUpdateDestroyAPIView.as_view(), name='tweet_retrieve_update_destroy')
]
