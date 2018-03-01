# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-01 03:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20180301_0238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='_validation_str',
            field=models.CharField(default='ZEFTON83EARPK5VYH3OY6UH2T557I7ZYXGRDUNAE6YANNKAQTVS3U8DM6O5KA406C45VCMBDEOP8ZHP7FCIRN5PHIFAOS8QSEDX3', editable=False, max_length=100, verbose_name='Validation string'),
        ),
        migrations.AlterField(
            model_name='student',
            name='referral_link',
            field=models.CharField(default='LIPR2ID4ZB5NWKX3S06H4VCWEDSP955HDZMDKC4JVAWHCB4BT26F3YXQ4K63KO8L4WUV9P4FH1MUQT3QMZREV70D8Z7FVEIIBZQD', editable=False, max_length=100, verbose_name='referral_link'),
        ),
        migrations.RemoveField(
            model_name='student',
            name='referrer_students',
        ),
        migrations.AddField(
            model_name='student',
            name='referrer_students',
            field=models.ManyToManyField(null=True, related_name='_student_referrer_students_+', to='core.Student'),
        ),
    ]
