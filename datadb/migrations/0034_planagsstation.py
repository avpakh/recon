# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0033_gstation'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanAgsStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geom', djgeojson.fields.PointField()),
                ('description', models.TextField()),
                ('description_ru', models.TextField()),
                ('station_id', models.IntegerField()),
                ('picture', models.ImageField(upload_to=b'')),
                ('explanation', models.TextField()),
            ],
            options={
                'db_table': 'Pagstation',
                'managed': True,
            },
        ),
    ]
