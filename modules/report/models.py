from django.db import models


# Create your models here.


class Report(models.Model):
    name = models.CharField(verbose_name="Название", max_length=300)
    report_file = models.FileField(verbose_name="Отчет", upload_to='report')
    create_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    create_by = models.ForeignKey('account.Account', verbose_name='Кем создано', on_delete=models.CASCADE)
