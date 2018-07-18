from django.contrib import admin
from .models import Tag
from .models import TaggedItem


# Register your models here.

class TagAdmin(admin.ModelAdmin):
    pass


class TaggedItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)
admin.site.register(TaggedItem, TaggedItemAdmin)
