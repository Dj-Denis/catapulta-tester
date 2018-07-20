from django.contrib import admin

from .models import Plan
from .models import PlanCases
from .models import PlanLog


# Register your tags here.

class PlanAdmin(admin.ModelAdmin):
    pass


class PlanLogAdmin(admin.ModelAdmin):
    pass


class PlanCasesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Plan, PlanAdmin)
admin.site.register(PlanLog, PlanLogAdmin)
admin.site.register(PlanCases, PlanCasesAdmin)