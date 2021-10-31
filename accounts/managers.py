from django.db import models
from django.contrib.auth.models import UserManager as BaseUserManager
from django.http import Http404
from django.shortcuts import get_object_or_404


class UserManager(BaseUserManager):
    pass


class FollowManager(models.Manager):
    def follow(self, user, follower):
        if user == follower:
            raise Http404
        instance, created = self.get_or_create(user=user, follower=follower)
        not created and not instance.is_followed and instance.follow()
        return instance

    def unfollow(self, user, follower):
        instance = get_object_or_404(self.model, user=user, follower=follower)
        instance.is_followed and instance.unfollow()
        return instance
