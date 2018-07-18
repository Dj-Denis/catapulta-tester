# Generated by Django 2.0.7 on 2018-07-17 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('test_plans', '0004_plancases_run_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plancases',
            name='run_by',
        ),
        migrations.AddField(
            model_name='planlog',
            name='run_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Запущен'),
            preserve_default=False,
        ),
    ]
