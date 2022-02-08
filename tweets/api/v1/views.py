from django.contrib.auth import get_user_model

from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404
)
from rest_framework.permissions import IsAuthenticated

from core.api.permissions import IsOwnerOrReadOnly
from tweets.api.v1.serializers import TagSerializer, TweetSerializer
from tweets.models import Tag, Tweet

User = get_user_model()


class TagListAPIView(ListAPIView):
    pagination_class = None
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class TweetListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TweetSerializer

    def get_queryset(self):
        """
        Filters tweets based on request
        Scenarios:
            1. username passed as query_param -> Returns tweets by the user that matches the username
            2. is_followers passed as query_param -> Returns tweets by the followers of requested users
            3. Otherwise, returns tweets by the users whom the requested user follows
        :return: QuerySet of Tweet Instances
        """

        username = self.request.query_params.get('username')
        is_followers = bool(self.request.query_params.get('is_followers', False))

        if username:
            user = get_object_or_404(User, username=username)
            return user.tweets.all().select_related('user').prefetch_related('tags')
        elif is_followers:
            return Tweet.objects.follower_tweets(self.request.user)
        return Tweet.objects.followed_users_tweets(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TweetRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TweetSerializer

    def get_object(self):
        tweet = get_object_or_404(Tweet, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, tweet.user)
        return tweet
