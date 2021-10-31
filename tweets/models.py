from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import AbstractTimestampModel


class Tag(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=60)

    class Meta:
        verbose_name = _('Tags')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.title


class Tweet(AbstractTimestampModel):
    user = models.ForeignKey(
        verbose_name=_('User'),
        to=settings.AUTH_USER_MODEL,
        related_name='tweets',
        on_delete=models.CASCADE
    )
    content = models.CharField(verbose_name=_('Content'), max_length=120)
    tags = models.ManyToManyField(
        verbose_name=_('Tags'),
        to='Tag',
        related_name='tweets',
        blank=True
    )

    class Meta:
        verbose_name = _('Tweet')
        verbose_name_plural = _('Tweets')

    def __str__(self):
        return self.content
