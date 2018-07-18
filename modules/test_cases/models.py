from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse


# Create your tags here.

class Case(models.Model):
    CASE_STATUS_CHOICES = (
        ('0', 'Не выполнялось'),
        ('1', 'Успешно'),
        ('2', 'Провалено')
    )

    name = models.CharField(verbose_name="Имя", blank=False, max_length=100)
    description = models.TextField(verbose_name="Описание", blank=True, default='')
    create_by = models.ForeignKey('account.Account', on_delete=models.CASCADE, verbose_name='Автор')
    precondition = models.TextField(verbose_name="Предварительные условия", blank=True, default='')
    excepted_result = models.TextField(verbose_name="Ожидаемый результат")
    status = models.CharField(max_length=20, verbose_name='Статус', choices=CASE_STATUS_CHOICES, default='0')
    comment = models.TextField(verbose_name='Коментарий', blank=True, default='')
    last_run = models.DateTimeField(verbose_name="Последний запуск", blank=True, null=True)

    create_at = models.DateTimeField(verbose_name="Создан", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Изменен", auto_now=True)

    related_tag = GenericRelation('tags.TaggedItem')

    class Meta:
        verbose_name = "Кейс"
        verbose_name_plural = 'Кейсы'
        permissions = (
            ('edit_case', 'Может редактировать кейсы'),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('case_detail', args=[str(self.id)])

    @property
    def last_log(self):
        return self.caselog_set.filter().last()


class CaseLog(models.Model):
    CASE_STATUS_CHOICES = (
        ('0', 'Успешно'),
        ('1', 'Провалено')
    )
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name='Кейс')
    comment = models.TextField(verbose_name='Коментарий')
    date = models.DateTimeField(verbose_name='Дата', auto_now_add=True)
    status = models.CharField(max_length=20, verbose_name='Статус', choices=CASE_STATUS_CHOICES, default='0')
    run_by = models.ForeignKey('account.Account', on_delete=models.CASCADE, verbose_name='Запускал')

    class Meta:
        verbose_name = "Лог кейса"
        verbose_name_plural = 'Логи кейсов'

    def __str__(self):
        return self.case.name
