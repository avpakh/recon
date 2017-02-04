# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prognoz', '0039_prognozgraph_brovka1'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapsdata',
            name='addF',
            field=models.TextField(default=1, verbose_name=b'AddF'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='prognozgraph',
            name='brovka',
            field=models.DecimalField(verbose_name=b' \xd0\xa3\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd0\xbd\xd1\x8c \xd0\xbe\xd1\x82\xd0\xbd\xd0\xbe\xd1\x81\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xbe \xd0\xb1\xd1\x80\xd0\xbe\xd0\xb2\xd0\xba\xd0\xb8, \xd0\xbc', max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='prognozgraph',
            name='brovka1',
            field=models.DecimalField(verbose_name=b'\xd0\xa3\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd0\xbd\xd1\x8c \xd0\xbe\xd1\x82\xd0\xbd\xd0\xbe\xd1\x81\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xbe \xd0\xb1\xd1\x80\xd0\xbe\xd0\xb2\xd0\xba\xd0\xb8', max_digits=5, decimal_places=2),
        ),
    ]
