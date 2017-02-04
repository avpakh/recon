# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prognoz', '0037_mapsbrovka_brovka_value'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mapsbrovka',
            old_name='brovka0_50',
            new_name='brovka1',
        ),
        migrations.RenameField(
            model_name='mapsbrovka',
            old_name='brovka50_80',
            new_name='brovka2',
        ),
        migrations.RenameField(
            model_name='mapsbrovka',
            old_name='brovka80_200',
            new_name='brovka3',
        ),
        migrations.RenameField(
            model_name='mapsbrovka',
            old_name='brovka200',
            new_name='brovka4',
        ),
    ]
