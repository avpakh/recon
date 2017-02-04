# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0035_gstation_urlname'),
    ]

    operations = [
        migrations.AddField(
            model_name='gstation',
            name='txtdata',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
