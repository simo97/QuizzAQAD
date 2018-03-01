# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-01 02:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20180301_0237'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='_validation_str',
            field=models.CharField(default='0B6431AEEU3KSZ32TLF68Y0KVKYWEG17NVL9UYUXJKTNGKBMP0ZA2TDKYQ5Q0P4XQ9UKTR01JJZBIE6Z7O552A8FKIS8CXKFS8Y0', editable=False, max_length=100, verbose_name='Validation string'),
        ),
        migrations.AddField(
            model_name='student',
            name='referral_link',
            field=models.CharField(default='39J4V2JCF3BXSBNK8V1ME9XJQ68WA2Y3POE6WM1RU7DO3KSL2ZLG7AGS3AOCS3IH9D9CZ7AOOGYXCXETPMETIWMEM15SW6ZMFKB8', editable=False, max_length=100, verbose_name='referral_link'),
        ),
    ]
