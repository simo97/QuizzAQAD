# Generated by Django 2.0.3 on 2018-03-10 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20180307_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='_validation_str',
            field=models.CharField(default='QV2UEKG1HCHC5IQC960RLOW39BACPCP5RGIB1Z2RES0HOR8JEM4U9THU9R4A0XCOLNIN8S0Q6E0SZPFZTGEAI8ISTYAH0WX80K5H', editable=False, max_length=100, verbose_name='Validation string'),
        ),
        migrations.AlterField(
            model_name='student',
            name='referral_link',
            field=models.CharField(default='83JUR1S559K3OX0QNSBSVXKDSBK8FQK04NJSFTXLTR6EAK5KWDDPU6FYK1CE13HIDW43Q6648LOJDKINQ76OE2JNAZ9IQHVYJ488', editable=False, max_length=100, verbose_name='referral_link'),
        ),
    ]
