from django.db import models
from django.contrib.auth.models import UserManager as BaseUserManager
from django.http import Http404
from django.shortcuts import get_object_or_404


class UserManager(BaseUserManager):
    pass


class FollowManager(models.Manager):
    def follow(self, user, follower):
        """
        Follow a user, If the Follow entry is already created, mark is_followed as True
        :param user:
        :param follower:
        :return: Follow instance
        """

        if user == follower:
            raise Http404
        instance, created = self.get_or_create(user=user, follower=follower)
        not created and not instance.is_followed and instance.follow()
        return instance

    def unfollow(self, user, follower):
        """
        Unfollow a user, If the Follow entry is already created, mark is_followed as False
        :param user:
        :param follower:
        :return: Follow instance
        """

        instance = get_object_or_404(self.model, user=user, follower=follower)
        instance.is_followed and instance.unfollow()
        return instance
