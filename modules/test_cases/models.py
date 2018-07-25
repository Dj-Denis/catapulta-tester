from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

# Create your tags here.

class Case(models.Model):
    CASE_STATUS_CHOICES = (
        ('0', _('Не выполнялось')),
        ('1', _('Успешно')),
        ('2', _('Провалено'))
    )

    name = models.CharField(verbose_name=_("Имя"), blank=False, max_length=100)
    description = models.TextField(verbose_name=_("Описание"), blank=True, default='')
    create_by = models.ForeignKey('account.Account', on_delete=models.CASCADE, verbose_name=_('Автор'))
    precondition = models.TextField(verbose_name=_("Предварительные условия"), blank=True, default='')
    excepted_result = models.TextField(verbose_name=_("Ожидаемый результат"))
    status = models.CharField(max_length=20, verbose_name=_('Статус'), choices=CASE_STATUS_CHOICES, default='0')
    comment = models.TextField(verbose_name=_('Коментарий'), blank=True, default='')
    last_run = models.DateTimeField(verbose_name=_("Последний запуск"), blank=True, null=True)

    create_at = models.DateTimeField(verbose_name=_("Создан"), auto_now_add=True)
    update_at = models.DateTimeField(verbose_name=_("Изменен"), auto_now=True)

    class Meta:
        verbose_name = _("Кейс")
        verbose_name_plural = _('Кейсы')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('case_detail', args=[str(self.id)])

    @property
    def last_log(self):
        return self.caselog_set.filter().last()

    @property
    def last_two_logs(self):
        return self.caselog_set.filter().order_by('-id')[:2][::-1]


class CaseLog(models.Model):
    CASE_STATUS_CHOICES = (
        ('0', _('Успешно')),
        ('1', _('Провалено'))
    )
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name=_('Кейс'))
    comment = models.TextField(verbose_name=_('Коментарий'))
    date = models.DateTimeField(verbose_name=_('Дата'), auto_now_add=True)
    status = models.CharField(max_length=20, verbose_name=_('Статус'), choices=CASE_STATUS_CHOICES, default='0')
    run_by = models.ForeignKey('account.Account', on_delete=models.CASCADE, verbose_name=_('Запускал'))

    class Meta:
        verbose_name = _("Лог кейса")
        verbose_name_plural = _('Логи кейсов')

    def __str__(self):
        return self.case.name
