# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prognoz', '0029_prognozgraph'),
    ]

    operations = [
        migrations.AddField(
            model_name='prognozgraph',
            name='dist_km',
            field=models.IntegerField(default=1, verbose_name=b' \xd0\xa0\xd0\xb0\xd1\x81\xd1\x81\xd1\x82\xd0\xbe\xd1\x8f\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb4\xd0\xbe \xd1\x83\xd1\x81\xd1\x82\xd1\x8c\xd1\x8f '),
            preserve_default=False,
        ),
    ]
