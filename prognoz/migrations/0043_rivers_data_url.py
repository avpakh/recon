# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prognoz', '0042_auto_20160503_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='rivers',
            name='data_url',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
