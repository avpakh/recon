# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0036_gstation_txtdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='agsstation',
            name='discharge',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
