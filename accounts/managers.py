from django.db import models
from django.contrib.auth.models import UserManager as BaseUserManager
from django.shortcuts import get_object_or_404


class UserManager(BaseUserManager):
    pass


class FollowManager(models.Manager):
    def follow(self, user, follower):
        instance, created = self.get_or_create(user=user, follower=follower)
        not created and instance.follow()
        return instance

    def unfollow(self, user, follower):
        instance, _ = get_object_or_404(self.model.__class__, user=user, follower=follower)
        instance.unfollow()
        return instance
