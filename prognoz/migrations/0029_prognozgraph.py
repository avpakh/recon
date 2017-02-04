# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prognoz', '0028_auto_20160405_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrognozGraph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('distance', models.DecimalField(verbose_name=b' \xd0\xa0\xd0\xb0\xd1\x81\xd1\x81\xd1\x82\xd0\xbe\xd1\x8f\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb4\xd0\xbe \xd1\x83\xd1\x81\xd1\x82\xd1\x8c\xd1\x8f ', max_digits=12, decimal_places=6)),
                ('discharge', models.DecimalField(verbose_name=b'\xd0\xa0\xd0\xb0\xd1\x81\xd1\x85\xd0\xbe\xd0\xb4 \xd1\x80\xd0\xb5\xd0\xba\xd0\xb8', max_digits=12, decimal_places=6)),
                ('level', models.DecimalField(verbose_name=b'\xd0\xa3\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd0\xbd\xd1\x8c \xd1\x80\xd0\xb5\xd0\xba\xd0\xb8', max_digits=12, decimal_places=6)),
                ('dno', models.DecimalField(verbose_name=b'\xd0\x9e\xd1\x82\xd0\xbc\xd0\xb5\xd1\x82\xd0\xba\xd0\xb0 \xd0\xb4\xd0\xbd\xd0\xb0', max_digits=12, decimal_places=6)),
                ('time60', models.DecimalField(verbose_name=b'\xd0\x92\xd1\x80\xd0\xb5\xd0\xbc\xd1\x8f \xd0\xb2 \xd1\x87\xd0\xb0\xd1\x81\xd0\xb0\xd1\x85:\xd0\xbc\xd0\xb8\xd0\xbd\xd1\x83\xd1\x82\xd0\xb0\xd1\x85', max_digits=5, decimal_places=2)),
                ('time100', models.DecimalField(verbose_name=b'\xd0\x92\xd1\x80\xd0\xb5\xd0\xbc\xd1\x8f \xd0\xb2 \xd1\x87\xd0\xb0\xd1\x81\xd0\xb0\xd1\x85', max_digits=5, decimal_places=2)),
                ('brovka', models.DecimalField(verbose_name=b'\xd0\x9f\xd1\x80\xd0\xb5\xd0\xb2\xd1\x8b\xd1\x88\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xbd\xd0\xb0\xd0\xb4 \xd0\xb1\xd1\x80\xd0\xbe\xd0\xb2\xd0\xba\xd0\xbe\xd0\xb9', max_digits=5, decimal_places=2)),
                ('label', models.TextField(max_length=120, verbose_name=b'\xd0\xa8\xd0\xba\xd0\xb0\xd0\xbb\xd0\xb0')),
            ],
            options={
                'db_table': 'PrognozGraph',
                'managed': True,
            },
        ),
    ]
