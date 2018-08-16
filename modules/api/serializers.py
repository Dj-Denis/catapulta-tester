import django_rq
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from registration.models import RegistrationProfile
from registration.signals import user_registered, user_activated
from rest_framework import serializers

from modules.account.models import Account
from modules.report.models import Report
from modules.report.tasks import create_report
from modules.tags.models import TaggedItem, Tag
from modules.test_cases.models import Case, CaseLog
from modules.test_plans.models import Plan, PlanCases, PlanLog


class AccountSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'second_name', 'email', 'full_name')

    def get_full_name(self, obj):
        return obj.get_full_name()


class TagItemField(serializers.RelatedField):

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return value.name


class TaggedItemSerializer(serializers.ModelSerializer):
    tag = TagItemField(read_only=True)

    class Meta:
        model = TaggedItem
        fields = ('tag',)


class TaggedRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        return Tag.objects.get(pk=data)

    def to_representation(self, value):
        serializer = TaggedItemSerializer(value)
        return serializer.data


class CaseSerializer(serializers.ModelSerializer):
    create_by = AccountSerializer(read_only=True)
    tag_list = TaggedRelatedField(queryset=TaggedItem.objects.all(), many=True, required=False)
    id = serializers.IntegerField(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = (
        'id', 'name', 'description', 'precondition', 'excepted_result', 'comment', 'create_by', 'tag_list', 'url')

    def create(self, validated_data):
        user = self.context['request'].user
        case = Case.objects.create(**validated_data, create_by=user)
        return case

    def update(self, instance, validated_data):
        tag_list = validated_data.pop('tag_list')
        for tag in tag_list:
            TaggedItem.objects.create(tag=tag, content_type=ContentType.objects.get_for_model(instance),
                                      object_id=instance.pk)
        return super(CaseSerializer, self).update(instance, validated_data)

    def get_url(self, obj):
        return obj.get_absolute_url()


class CaseLogSerializer(serializers.ModelSerializer):
    run_by = AccountSerializer(read_only=True)
    case = CaseSerializer(read_only=True)

    class Meta:
        model = CaseLog
        fields = ('case', 'comment', 'run_by', 'status')


class PlanLogRelatedSerializer(serializers.ModelSerializer):
    last_run = serializers.DateTimeField(read_only=True)
    run_by = AccountSerializer(read_only=True)
    caselog_set = CaseLogSerializer(read_only=True, many=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = PlanLog
        fields = ('id', 'plan', 'comment', 'status', 'run_by', 'last_run', 'caselog_set', 'url')

    def get_url(self, obj):
        return obj.get_absolute_url()


class PlanLogSerializer(serializers.ModelSerializer):
    last_run = serializers.DateTimeField(read_only=True)
    run_by = AccountSerializer(read_only=True)
    caselog_set = serializers.SerializerMethodField('paginated_caselog')

    class Meta:
        model = PlanLog
        fields = ('id', 'plan', 'comment', 'status', 'run_by', 'last_run', 'caselog_set')

    def paginated_caselog(self, obj):
        page_size = 10
        paginator = Paginator(obj.caselog_set.all(), page_size)
        page = self.context['request'].query_params.get('page') or 1
        logs = paginator.page(page)
        serializers = CaseLogSerializer(logs, many=True)
        return serializers.data


class PlanSerializer(serializers.ModelSerializer):
    # create_by = serializers.HyperlinkedRelatedField(view_name='account_detail', read_only=True)
    create_by = AccountSerializer()
    cases = serializers.HyperlinkedRelatedField(view_name='case_detail_api', many=True, read_only=True)
    id = serializers.IntegerField(read_only=True)
    planlog_set = serializers.HyperlinkedRelatedField(view_name='plan_log', read_only=True, many=True)
    success = serializers.SerializerMethodField()
    failed = serializers.SerializerMethodField()
    run_by = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ('id', 'name', 'description', 'status', 'create_at', 'update_at', 'create_by', 'cases', 'planlog_set',
                  'success', 'failed', 'run_by')

    def create(self, validated_data):
        user = self.context['request'].user
        plan = Plan.objects.create(**validated_data, create_by=user)
        return plan

    def get_success(self, obj):
        last_log = obj.last_log
        if last_log:
            return last_log.get_success.count()
        else:
            return '0'

    def get_failed(self, obj):
        last_log = obj.last_log
        if last_log:
            return last_log.get_failed.count()
        else:
            return '0'

    def get_run_by(self, obj):
        last_log = obj.last_log
        if last_log:
            return AccountSerializer(last_log.run_by).data
        else:
            return {}

class PlanDetailSerializer(serializers.ModelSerializer):
    # planlog_set = serializers.HyperlinkedModelSerializer()

    class Meta:
        model = Plan
        fields = ('id', 'name', 'description', 'status', 'create_at', 'update_at', 'create_by', 'cases', 'planlog_set')

    def paginated_planlog(self, obj):
        page_size = 10
        paginator = Paginator(obj.planlog_set.all(), page_size)
        page = self.context['request'].query_params.get('page') or 1
        logs = paginator.page(page)
        serializers = PlanLogSerializer(logs, many=True)

        return serializers.data


class CaseLogRelatedSerializer(serializers.ModelSerializer):
    run_by = AccountSerializer(read_only=True)
    case = CaseSerializer()
    url = serializers.SerializerMethodField()

    class Meta:
        model = CaseLog
        fields = ('case', 'comment', 'run_by', 'status', 'date', 'url')

    def get_url(self, obj):
        url = PlanLog.objects.get(caselog=obj).get_absolute_url()
        return url


class CasePlanRelatedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    url = serializers.SerializerMethodField()
    last_run = serializers.SerializerMethodField()
    run_by = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()


    class Meta:
        model = Case
        fields = (
            'id', 'name', 'description', 'precondition', 'excepted_result', 'comment', 'url', 'last_run', "run_by", "status")

    def __init__(self, *args, **kwargs):
        # print(kwargs['context'])
        super(CasePlanRelatedSerializer, self).__init__(*args, **kwargs)
        self.plan_id = self.context['request'].parser_context['kwargs']['pk']

    def get_last_run(self, obj):
        case_log = CaseLog.objects.filter(plan_run_log__plan_id=self.plan_id, case_id=obj.pk).last()
        if case_log is not None:
            return case_log.date
        else:
            return ''

    def get_run_by(self, obj):
        case_log = CaseLog.objects.filter(plan_run_log__plan_id=self.plan_id, case_id=obj.pk).last()
        if case_log is not None:
            return case_log.run_by.get_full_name()
        else:
            return ''

    def get_status(self, obj):
        case_log = CaseLog.objects.filter(plan_run_log__plan_id=self.plan_id, case_id=obj.pk).last()
        if case_log is not None:
            return case_log.status
        else:
            return 'Не запускалось'

    def get_url(self, obj):
        return obj.get_absolute_url()


class PlanUpdateSerializer(serializers.ModelSerializer):
    create_by = serializers.HyperlinkedRelatedField(view_name='account_detail', read_only=True)
    cases = serializers.PrimaryKeyRelatedField(queryset=Case.objects.all(), many=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Plan
        fields = ('id', 'name', 'description', 'status', 'create_at', 'update_at', 'create_by', 'cases')

    def create(self, validated_data):
        user = self.context['request'].user

        plan = Plan.objects.create(**validated_data, create_by=user)
        return plan

    def update(self, instance, validated_data):
        cases = validated_data.pop('cases', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        for case in cases:
            PlanCases.objects.create(plan=instance, case=case)
        instance.save()
        return instance


class PlanCaseSerializer(serializers.ModelSerializer):
    case = serializers.PrimaryKeyRelatedField(many=True, queryset=Case.objects.all(), write_only=True)

    class Meta:
        model = PlanCases
        fields = ('plan', 'case')

    def create(self, validated_data):
        plan = validated_data['plan']
        cases = validated_data['case']
        plan_case = PlanCases.objects.last()
        for case in cases:
            plan_case = PlanCases.objects.create(plan=plan, case=case)
        return plan_case


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'password', 'first_name', 'second_name')

    def create(self, validated_data):
        new_user = Account.objects.create_user(email=validated_data['email'], password=validated_data['password'])
        new_user.first_name = validated_data['first_name']
        new_user.second_name = validated_data['second_name']
        new_user.save()
        user = RegistrationProfile.objects.create_inactive_user(new_user=new_user,
                                                                site=get_current_site(self.context['request']),
                                                                send_email=True,
                                                                request=self.context['request'])
        user_registered.send(sender=self.__class__,
                             user=user,
                             request=self.context['request'])
        return new_user


class ActivationSerializer(serializers.Serializer):
    activation_key = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        pass

    class Meta:
        fields = ('activation_key',)

    def create(self, validated_data):
        user, activated = RegistrationProfile.objects.activate_user(**validated_data,
                                                                    site=get_current_site(self.context['request']))
        if activated:
            user_activated.send(sender=self.__class__,
                                user=user,
                                request=self.context['request'])
        return user


class ReportSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=300, write_only=True)
    status = serializers.CharField(max_length=30, read_only=True)

    class Meta:
        model = Report
        fields = ('name', 'status')

    def create(self, validated_data):
        queue = django_rq.get_queue('default')
        queue.enqueue(create_report, validated_data['name'], self.context['request'].user)
        return {'status': '1'}
