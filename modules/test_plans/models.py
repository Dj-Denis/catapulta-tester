from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


# Create your tags here.


class Plan(models.Model):
    PLAN_STATUS_CHOICES = (
        ('0', _('Не выполнялось')),
        ('1', _('Успешно')),
        ('2', _('Провалено'))
    )
    name = models.CharField(verbose_name=_("Имя"), blank=False, max_length=300)
    description = models.TextField(verbose_name=_("Описание"))
    create_at = models.DateTimeField(verbose_name=_("Создан"), auto_now_add=True)
    update_at = models.DateTimeField(verbose_name=_("Изменен"), auto_now=True)
    status = models.CharField(max_length=30, choices=PLAN_STATUS_CHOICES, default='0')
    create_by = models.ForeignKey('account.Account', on_delete=models.CASCADE, verbose_name=_('Создан'))
    cases = models.ManyToManyField('test_cases.Case', through='PlanCases')
    last_run = models.DateTimeField(verbose_name=_("Последний запуск"), blank=True, null=True)



    class Meta:
        verbose_name = _("План")
        verbose_name_plural = _('Планы')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plan_detail', args=[str(self.id)])

    @property
    def last_log(self):
        return self.planlog_set.filter().last()



class PlanCases(models.Model):
    CASE_STATUS_CHOICES = (
        ('0', _('Не выполнялось')),
        ('1', _('Успешно')),
        ('2', _('Провалено'))
    )
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    case = models.ForeignKey('test_cases.Case', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=CASE_STATUS_CHOICES, default='0')
    comment = models.TextField(verbose_name=_("Коментарий"), blank=True, default='')

    class Meta:
        verbose_name = _("Связь")
        verbose_name_plural = _("Связи")

    def __str__(self):
        return "%s - %s" % (self.plan.name, self.case.name)


class PlanLog(models.Model):
    PLAN_STATUS_CHOICES = (
        ('0', _('Провалено')),
        ('1', _('Успешно'))
    )
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name=_('План'))
    comment = models.TextField(verbose_name=_("Коментарий"), blank=True, default='')
    status = models.CharField(max_length=30, choices=PLAN_STATUS_CHOICES, default='1')
    last_run = models.DateTimeField(verbose_name=_('Дата'), auto_now_add=True)
    run_by = models.ForeignKey('account.Account', on_delete=models.CASCADE, verbose_name=_('Запущен'))

    class Meta:
        verbose_name = _("Лог плана")
        verbose_name_plural = _('Логи планов')

    def __str__(self):
        return self.plan.name

    def get_absolute_url(self):
        return reverse('plan_log', args=[str(self.id)])

    @property
    def get_success(self):
        return self.caselog_set.filter(status='1')

    @property
    def get_failed(self):
        return self.caselog_set.filter(status='0')
