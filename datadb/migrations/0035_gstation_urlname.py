# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0034_planagsstation'),
    ]

    operations = [
        migrations.AddField(
            model_name='gstation',
            name='urlname',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
