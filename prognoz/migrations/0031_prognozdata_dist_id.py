# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prognoz', '0030_prognozgraph_dist_km'),
    ]

    operations = [
        migrations.AddField(
            model_name='prognozdata',
            name='dist_id',
            field=models.IntegerField(default=1, verbose_name=b'Id'),
            preserve_default=False,
        ),
    ]
