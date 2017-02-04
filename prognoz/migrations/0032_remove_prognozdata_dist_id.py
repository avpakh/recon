# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prognoz', '0031_prognozdata_dist_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prognozdata',
            name='dist_id',
        ),
    ]
