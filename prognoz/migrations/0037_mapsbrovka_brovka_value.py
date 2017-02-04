# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prognoz', '0036_mapsbrovka_dist_km'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapsbrovka',
            name='brovka_value',
            field=models.DecimalField(null=True, verbose_name=b'\xd0\xa3\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd0\xbd\xd1\x8c', max_digits=5, decimal_places=2, blank=True),
        ),
    ]
