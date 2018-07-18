# Generated by Django 2.0.6 on 2018-07-13 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20180713_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='group',
            field=models.ForeignKey(blank=True, default=3, help_text='Группа к которой принадлежит пользователь', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='user_set', related_query_name='user', to='account.CustomGroup', verbose_name='Группа'),
        ),
    ]
