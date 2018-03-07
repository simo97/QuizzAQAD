# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-07 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20180307_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='image_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='_validation_str',
            field=models.CharField(default='P9GSPX7A32QNTBD4263T3AG2EF1CXGF3E6LMCUWJJ8RYW970ASA5DN3AWJE6L5LT2W5TUL843UZZ7L7GQJKUD9VSBSCKJC5NLVP5', editable=False, max_length=100, verbose_name='Validation string'),
        ),
        migrations.AlterField(
            model_name='student',
            name='referral_link',
            field=models.CharField(default='ICM4CZ017SRNUS0SWHZQRW9WAV1R8CPQWT1L2CV3TA8LYL4EBP8716EGOIRURS7NUL7G65CVOIIKB89FRESL1E7AAZG12REGMP61', editable=False, max_length=100, verbose_name='referral_link'),
        ),
    ]
