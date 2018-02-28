# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-27 16:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20180225_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='notationhistory',
            name='choice',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='core.Choice'),
        ),
        migrations.AddField(
            model_name='notationhistory',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='notationhistory',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notations', to='core.Question'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='choicies', to='core.Question'),
        ),
    ]
