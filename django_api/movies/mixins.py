import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name=_('created_at'), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(
        verbose_name=_('modified_at'), auto_now=True, blank=True, null=True)


class UUIDMixin(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
