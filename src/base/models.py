from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        _("created date"),
        default=timezone.now,
        editable=False,
    )
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)
    created_by = models.ForeignKey("auth.User", on_delete=models.PROTECT)

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
