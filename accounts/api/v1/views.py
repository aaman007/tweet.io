from django.contrib.auth import get_user_model
from django.db.models import Count, Q

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, get_object_or_404

from accounts.api.v1.serializers import (
    UserSerializer,
    SingleUserSerializer,
    FollowSerializer,
    RegisterSerializer
)
from accounts.models import Follow

User = get_user_model()


class AbstractBaseFollowListAPIView(ListAPIView):
    serializer_class = FollowSerializer

    class Meta:
        abstract = True

    def get_permissions(self):
        if self.request.query_params.get('username'):
            self.permission_classes = []
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        username = self.request.query_params.get('username')
        if not username:
            return self.request.user.active_followers()
        user = get_object_or_404(User, username=username)
        return user.active_followers()


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token_type': 'Bearer',
            'token': token.key,
            'user': UserSerializer(instance=user).data
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token_type': 'Bearer',
            'token': token.key,
            'user': UserSerializer(instance=user).data
        })


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return list of user that the current user can follow
        Requires annotating followers_count and follows count for each user
        :return: QuerySet of User instances
        """
        following_ids = list(self.request.user.active_follows().values_list('user_id', flat=True))
        following_ids.append(self.request.user.id)
        return User.objects.exclude(id__in=following_ids).annotate(
            followers_count=Count('followers'),
            follows_count=Count('follows')
        ).only('username', 'first_name', 'last_name')


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = SingleUserSerializer
    lookup_field = 'username'

    def get_object(self):
        username = self.kwargs.get('username', '')
        user = get_object_or_404(User, username=username)
        return user


class FollowerListAPIView(AbstractBaseFollowListAPIView):
    pass


class FollowingListAPIView(AbstractBaseFollowListAPIView):
    def get_queryset(self):
        username = self.request.query_params.get('username')
        if not username:
            return self.request.user.active_follows()
        user = get_object_or_404(User, username=username)
        return user.active_follows()


class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        username = kwargs.get('username', '')
        user = get_object_or_404(User, username=username)
        if user == request.user:
            return Response({
                'error': 'Invalid user.'
            }, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.follow(user, request.user)
        return Response(UserSerializer(user, context={'request': request}).data)


class UnfollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        username = kwargs.get('username', '')
        user = get_object_or_404(User, username=username)
        if user == request.user:
            return Response({
                'error': 'Invalid user.'
            }, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.unfollow(user, request.user)
        return Response(UserSerializer(user, context={'request': request}).data)
