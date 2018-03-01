# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-01 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20180227_2353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='referral_link',
        ),
        migrations.AddField(
            model_name='student',
            name='_is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='notationhistory',
            name='month',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_month_vote',
            field=models.IntegerField(default=3),
        ),
    ]