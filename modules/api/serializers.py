from django.contrib.sites.shortcuts import get_current_site
from registration.models import RegistrationProfile
from registration.signals import user_registered, user_activated
from rest_framework import serializers

from modules.account.models import Account
from modules.tags.models import TaggedItem
from modules.test_cases.models import Case
from modules.test_plans.models import Plan, PlanCases


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'first_name', 'second_name', 'email')


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
        pass

    def to_representation(self, value):
        serializer = TaggedItemSerializer(value)
        return serializer.data


class CaseSerializer(serializers.ModelSerializer):
    create_by = serializers.HyperlinkedRelatedField(view_name='account_detail', read_only=True)
    tag_list = TaggedRelatedField(queryset=TaggedItem.objects.all(), many=True, required=False)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Case
        fields = ('id', 'name', 'description', 'precondition', 'excepted_result', 'comment', 'create_by', 'tag_list')

    def create(self, validated_data):
        user = self.context['request'].user
        case = Case.objects.create(**validated_data, create_by=user)
        return case

    def update(self, instance, validated_data):
        print(instance)
        print(validated_data)
        return super(CaseSerializer, self).update(instance, validated_data)


class PlanSerializer(serializers.ModelSerializer):
    create_by = serializers.HyperlinkedRelatedField(view_name='account_detail', read_only=True)
    cases = serializers.HyperlinkedRelatedField(view_name='case_detail', many=True, read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Plan
        fields = ('id', 'name', 'description', 'status', 'create_at', 'update_at', 'create_by', 'cases')

    def create(self, validated_data):
        user = self.context['request'].user
        plan = Plan.objects.create(**validated_data, create_by=user)
        return plan


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
        print(validated_data)
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
        print(validated_data)
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
        print(validated_data)
        user, activated = RegistrationProfile.objects.activate_user(**validated_data,
                                                                    site=get_current_site(self.context['request']))
        if activated:
            user_activated.send(sender=self.__class__,
                                user=user,
                                request=self.context['request'])
        return user
