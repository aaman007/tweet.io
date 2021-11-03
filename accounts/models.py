from django.db import models
from django.contrib.auth.models import AbstractUser as BaseUser
from django.utils.translation import gettext_lazy as _

from core.models import AbstractTimestampModel
from accounts.managers import UserManager, FollowManager


class User(BaseUser):
    objects = UserManager()

    class Meta:
        ordering = ['-id']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return self.get_full_name()

    def active_followers(self):
        return self.followers.filter(is_followed=True)

    def active_follows(self):
        return self.follows.filter(is_followed=True)


class Follow(AbstractTimestampModel):
    user = models.ForeignKey(
        verbose_name=_('User'),
        to='User',
        related_name='followers',
        on_delete=models.CASCADE
    )
    follower = models.ForeignKey(
        verbose_name=_('Follower'),
        to='User',
        related_name='follows',
        on_delete=models.CASCADE
    )
    is_followed = models.BooleanField(verbose_name=_('Is Followed?'), default=True)

    objects = FollowManager()

    class Meta:
        ordering = ['-id']
        verbose_name = _('Follow')
        verbose_name_plural = _('Follows')
        unique_together = ('user', 'follower')

    def follow(self):
        self.is_followed = True
        self.save(update_fields=['is_followed'])

    def unfollow(self):
        self.is_followed = False
        self.save(update_fields=['is_followed'])
