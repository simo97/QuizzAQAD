# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-03 20:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20180301_0500'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField(default='About', null=True)),
                ('footer_left', models.TextField(default='left content', null=True)),
                ('footer_center', models.TextField(default='center content', null=True)),
                ('footer_right', models.TextField(default='right content', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='_validation_str',
            field=models.CharField(default='6D45FUS8DDA346NHGMZEXTAV8DRY2UHE6X80Q3S3DM0EQHXJN8NR48G8NRYYXKLBQZF4TETG0VF4A2DMTA7MW0OWFP1VHVVEUI9C', editable=False, max_length=100, verbose_name='Validation string'),
        ),
        migrations.AlterField(
            model_name='student',
            name='referral_link',
            field=models.CharField(default='WBGY7SH12OHW3DY0OOTDQOMD5NTUD691BLBYPVTQP6TTUBMNBV9LJ0NW513VHGJJVWDRGDO0RSWM2P8I1D9CLOUFBD6H327FWZYF', editable=False, max_length=100, verbose_name='referral_link'),
        ),
        migrations.AlterField(
            model_name='student',
            name='referrer_students',
            field=models.ManyToManyField(related_name='_student_referrer_students_+', to='core.Student'),
        ),
    ]
