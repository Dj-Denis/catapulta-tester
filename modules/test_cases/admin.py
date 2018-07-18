from django.contrib import admin
from .models import Case
from .models import CaseLog


# Register your tags here.


class CaseAdmin(admin.ModelAdmin):
    pass


class CaseLogAdmin(admin.ModelAdmin):
    pass


admin.site.register(Case, CaseAdmin)
admin.site.register(CaseLog, CaseLogAdmin)
