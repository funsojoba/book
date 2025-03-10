import uuid
from django.db import models
from django.http import Http404


def generate_id():
    return uuid.uuid4().hex


class BaseAbstractModel(models.Model):
    id = models.CharField(
        primary_key=True, editable=False, default=generate_id, max_length=70
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        "AUTHENTICATION.User",
        on_delete=models.CASCADE,
        verbose_name="created by",
        related_name="+",
        null=True,
        blank=True,
    )

    updated_by = models.ForeignKey(
        "AUTHENTICATION.User",
        on_delete=models.CASCADE,
        verbose_name="updated by",
        related_name="+",
        null=True,
        blank=True,
    )

    deleted_by = models.ForeignKey(
        "AUTHENTICATION.User",
        on_delete=models.CASCADE,
        verbose_name="deleted by",
        related_name="+",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ("-created_at",)

    def save(self, actor=None, *args, **kwargs):
        if not self.pk:
            self.created_by = actor
        super(BaseAbstractModel, self).save(*args, **kwargs)



def get_object_or_404(model, **kwargs):
    instance = model.objects.filter(**kwargs).first()
    if instance:
        return instance
    raise Http404