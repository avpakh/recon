# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0032_requestav_value_avgbcp'),
    ]

    operations = [
        migrations.CreateModel(
            name='GStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geom', djgeojson.fields.PointField()),
                ('description', models.TextField()),
                ('description_ru', models.TextField()),
                ('station_id', models.IntegerField()),
                ('value_level', models.DecimalField(max_digits=6, decimal_places=2)),
                ('value_brovka', models.FloatField()),
                ('value_bc', models.DecimalField(max_digits=6, decimal_places=2)),
                ('value_zero', models.FloatField()),
                ('picture', models.ImageField(upload_to=b'')),
                ('status', models.BooleanField()),
                ('explanation', models.TextField()),
                ('status_level', models.IntegerField()),
                ('datetime_text', models.TextField()),
            ],
            options={
                'db_table': 'Gstation',
                'managed': True,
            },
        ),
    ]
