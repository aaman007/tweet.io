from django.db import models


class AbstractTimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """ Ensures modified_at is updated when update_fields is passed """
        if update_fields and 'modified_at' not in update_fields:
            update_fields.append('modified_at')
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
