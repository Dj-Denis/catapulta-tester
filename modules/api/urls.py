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
    path('plan/<int:pk>', PlanDetailApi.as_view()),
    path('plan/<int:pk>/edit', PlanUpdateApi.as_view()),
    path('plan/<int:pk>/del', PlanDeleteApi.as_view()),
    path('case/', CaseListApi.as_view()),
    path('case/new', CaseCreateApi.as_view()),
    path('case/<int:pk>', CaseDetailApi.as_view(), name='case_detail'),
    path('case/<int:pk>/edit', CaseUpdateApi.as_view()),
    path('case/<int:pk>/del', CaseDeleteApi.as_view()),
    path('plan/link', PlanCasesApi.as_view()),
    path('register/', RegistrationApi.as_view()),
    path('activate/', ActivationApi.as_view()),
    path('report/', ReportsApi.as_view())
]