# Generated by Django 2.0.6 on 2018-07-10 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20180710_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/default-user.png', null=True, upload_to='avatars/', verbose_name='Аватар'),
        ),
    ]
