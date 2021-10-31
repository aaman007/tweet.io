from django.urls import path

from accounts.api.v1.views import (
    RegisterAPIView,
    LoginAPIView,
    UserRetrieveAPIView,
    FollowerListAPIView,
    FollowingListAPIView,
    FollowAPIView,
    UnfollowAPIView
)

app_name = 'accounts-api-v1'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('followers/', FollowerListAPIView.as_view(), name='followers'),
    path('following/', FollowingListAPIView.as_view(), name='following'),
    path('<str:username>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
    path('<str:username>/follow/', FollowAPIView.as_view(), name='follow'),
    path('<str:username>/unfollow/', UnfollowAPIView.as_view(), name='unfollow'),
]
