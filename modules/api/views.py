from registration.models import RegistrationProfile
from rest_framework import generics

from modules.account.models import Account
from modules.report.models import Report
from modules.test_cases.models import Case, CaseLog
from modules.test_plans.models import Plan, PlanCases, PlanLog
from .serializers import PlanSerializer, AccountSerializer, CaseSerializer, PlanCaseSerializer, PlanUpdateSerializer, \
    RegisterSerializer, ActivationSerializer, ReportSerializer, CaseLogSerializer, PlanLogSerializer, \
    PlanLogRelatedSerializer, CaseLogRelatedSerializer

# Create your views here.

"""
Account API`s
"""


class AccountDetailApi(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountListApi(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountCreateApi(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountUpdateApi(generics.UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDeleteApi(generics.DestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


"""
Plan API`s
"""


class PlanListApi(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class PlanDetailApi(generics.RetrieveAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class PlanCreateApi(generics.CreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class PlanUpdateApi(generics.UpdateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanUpdateSerializer


class PlanDeleteApi(generics.DestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class PlanLogCreateApi(generics.CreateAPIView):
    queryset = PlanLog.objects.all()
    serializer_class = PlanLogSerializer


class PlanLogReadApi(generics.RetrieveAPIView):
    queryset = PlanLog.objects.order_by('last_run')
    serializer_class = PlanLogSerializer


class PlanLogRelatedApi(generics.ListAPIView):
    queryset = PlanLog.objects.all().order_by('-last_run')
    serializer_class = PlanLogRelatedSerializer

    def get_queryset(self):
        q = self.queryset.filter(plan_id=self.kwargs['pk'])
        return q


"""
Case API`s
"""


class CaseDetailApi(generics.RetrieveAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


class CaseListApi(generics.ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


class CaseCreateApi(generics.CreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


class CaseUpdateApi(generics.UpdateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


class CaseDeleteApi(generics.DestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer


class CaseLogCreateApi(generics.CreateAPIView):
    queryset = CaseLog.objects.all()
    serializer_class = CaseLogSerializer


class CaseRelatedApi(generics.ListAPIView):
    serializer_class = CaseSerializer

    def get_queryset(self):
        return Case.objects.filter(plancases__plan_id=self.kwargs['pk'])


class CaseLogCaseRelatedApi(generics.ListAPIView):
    """
    Case logs related to specified case
    """
    queryset = CaseLog.objects.all().order_by('-date')
    serializer_class = CaseLogRelatedSerializer

    def get_queryset(self):
        q = self.queryset.filter(case_id=self.kwargs['pk'])
        return q


class CaseLogPlanRelatedApi(generics.ListAPIView):
    """
    Case logs related to specified plan log
    """
    queryset = CaseLog.objects.all().order_by('case_id')
    serializer_class = CaseLogRelatedSerializer

    def get_queryset(self):
        q = self.queryset.filter(plan_run_log_id=self.kwargs['pk'])
        return q


"""
Plan-Cases relation API`s
"""


class PlanCasesApi(generics.CreateAPIView):
    queryset = PlanCases.objects.all()
    serializer_class = PlanCaseSerializer


"""
Registration API`s
"""


class RegistrationApi(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = RegisterSerializer


class ActivationApi(generics.CreateAPIView):
    queryset = RegistrationProfile.objects.all()
    serializer_class = ActivationSerializer


class ReportsApi(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
