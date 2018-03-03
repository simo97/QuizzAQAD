# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-03 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20180303_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='mail',
            field=models.TextField(default='Mail template', null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='_validation_str',
            field=models.CharField(default='RK5TCMAHILPVH4DI7YSM2XT0E1UMH1BLWEB4NRA70AWBIXZXA46QR86RI53U51RV3XT4U05I32SKFJ0APHI7C0J9QU2106OHB3BG', editable=False, max_length=100, verbose_name='Validation string'),
        ),
        migrations.AlterField(
            model_name='student',
            name='referral_link',
            field=models.CharField(default='GE2YEBYCYI3K33WLCWZ2KUZMKJK4TCDEH78YPT51F694D207G82I5HGV6288V19P4W91J90TS94YW87310VE4WXIWS9JSPNVA5NU', editable=False, max_length=100, verbose_name='referral_link'),
        ),
    ]
