from django.urls import path

from .views import *

urlpatterns = [
    path('account/', AccountListApi.as_view()),
    path('account/new', AccountCreateApi.as_view()),
    path('account/<int:pk>', AccountDetailApi.as_view(), name='account_detail'),
    path('account/<int:pk>/edit', AccountUpdateApi.as_view()),
    path('account/<int:pk>/del', AccountDeleteApi.as_view()),
    path('plan/', PlanListApi.as_view()),
    path('plan/new', PlanCreateApi.as_view()),
    path('plan/<int:pk>', PlanDetailApi.as_view(), name='plan_detail_api'),
    path('plan/<int:pk>/edit', PlanUpdateApi.as_view()),
    path('plan/<int:pk>/del', PlanDeleteApi.as_view()),
    path('plan_log/new', PlanLogCreateApi.as_view()),
    path('plan_log/<int:pk>', PlanLogReadApi.as_view(), name='plan_log_api'),
    path('plan_log_rel/<int:pk>', PlanLogRelatedApi.as_view(), name='rel_plan_log'),
    path('case/', CaseListApi.as_view()),
    path('case/new', CaseCreateApi.as_view()),
    path('case/<int:pk>', CaseDetailApi.as_view(), name='case_detail_api'),
    path('case/<int:pk>/edit', CaseUpdateApi.as_view()),
    path('case/<int:pk>/del', CaseDeleteApi.as_view()),
    path('case_log/new', CaseLogCreateApi.as_view()),
    path('case_log_rel/case/<int:pk>', CaseLogCaseRelatedApi.as_view(), name='case_log_case_rel'),
    path('case_log_rel/plan/<int:pk>', CaseLogPlanRelatedApi.as_view(), name='case_log_plan_rel'),
    path('case_rel/plan/<int:pk>', CaseRelatedApi.as_view(), name='case_plan_rel'),
    path('plan/link', PlanCasesApi.as_view()),
    path('register/', RegistrationApi.as_view()),
    path('activate/', ActivationApi.as_view()),
    path('report/', ReportsApi.as_view())
]