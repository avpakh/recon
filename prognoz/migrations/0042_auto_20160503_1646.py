# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prognoz', '0041_floodset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floodset',
            name='distance',
            field=models.DecimalField(verbose_name=b' \xd0\xa0\xd0\xb0\xd1\x81\xd1\x81\xd1\x82\xd0\xbe\xd1\x8f\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb4\xd0\xbe \xd1\x83\xd1\x81\xd1\x82\xd1\x8c\xd1\x8f,  ', max_digits=12, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='floodset',
            name='level',
            field=models.DecimalField(null=True, verbose_name=b'\xd0\xa3\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd0\xbd\xd1\x8c \xd1\x80\xd0\xb5\xd0\xba\xd0\xb8, \xd0\xbc', max_digits=12, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='floodset',
            name='level_danger',
            field=models.DecimalField(null=True, verbose_name=b' \xd0\xa3\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd0\xbd\xd1\x8c \xd0\xbe\xd0\xbf\xd0\xb0\xd1\x81\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd0\xb8', max_digits=12, decimal_places=6),
        ),
    ]
