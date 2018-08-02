from django.contrib import admin

from .models import Report


# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    pass


admin.site.register(Report, ReportAdmin)
