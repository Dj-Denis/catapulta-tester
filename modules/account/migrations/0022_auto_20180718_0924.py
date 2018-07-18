# Generated by Django 2.0.7 on 2018-07-18 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_auto_20180718_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='groups',
            field=models.ForeignKey(blank=True, help_text='Группа к которой принадлежит пользователь', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_set', related_query_name='user', to='account.CustomGroup', verbose_name='Группа'),
        ),
    ]