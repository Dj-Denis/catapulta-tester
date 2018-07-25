from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name=_('Имя'))

    class Meta:
        verbose_name = _("Тег")
        verbose_name_plural = _('Теги')

    def __str__(self):
        return self.name

    @property
    def tagged_cont(self):
        return self.taggeditem_set.filter().count()


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag.name
