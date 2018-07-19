from django.db import models
from django.urls import reverse


# Create your tags here.


class Plan(models.Model):
    PLAN_STATUS_CHOICES = (
        ('0', 'Не выполнялось'),
        ('1', 'Успешно'),
        ('2', 'Провалено')
    )
    name = models.CharField(verbose_name="Имя", blank=False, max_length=300)
    description = models.TextField(verbose_name="Описание")
    create_at = models.DateTimeField(verbose_name="Создан", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Изменен", auto_now=True)
    status = models.CharField(max_length=30, choices=PLAN_STATUS_CHOICES, default='0')
    create_by = models.ForeignKey('account.Account', on_delete=models.CASCADE, verbose_name='Создан')
    cases = models.ManyToManyField('test_cases.Case', through='PlanCases')

    class Meta:
        verbose_name = "План"
        verbose_name_plural = 'Планы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plan_detail', args=[str(self.id)])

    @property
    def last_log(self):
        return self.planlog_set.filter().last()

    @property
    def succeed_count(self):
        return self.plancases_set.filter(case__status='1').count()

    @property
    def failed_count(self):
        return self.plancases_set.filter(case__status='2').count()


class PlanCases(models.Model):
    CASE_STATUS_CHOICES = (
        ('0', 'Не выполнялось'),
        ('1', 'Успешно'),
        ('2', 'Провалено')
    )
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    case = models.ForeignKey('test_cases.Case', on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=CASE_STATUS_CHOICES, default='0')
    comment = models.TextField(verbose_name="Коментарий", blank=True, default='')

    class Meta:
        verbose_name = "Отношение"
        verbose_name_plural = "Отношения"

    def __str__(self):
        return "%s - %s" % (self.plan.name, self.case.name)


class PlanLog(models.Model):
    PLAN_STATUS_CHOICES = (
        ('0', 'Успешно'),
        ('1', 'Провалено')
    )
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, verbose_name='План')
    comment = models.TextField(verbose_name="Коментарий")
    status = models.CharField(max_length=30, choices=PLAN_STATUS_CHOICES, default='0')
    last_run = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    run_by = models.ForeignKey('account.Account', on_delete=models.CASCADE, verbose_name='Запущен')

    class Meta:
        verbose_name = "Лог плана"
        verbose_name_plural = 'Логи планов'

    def __str__(self):
        return self.plan.name
