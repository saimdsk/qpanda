# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qpanda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.CharField(max_length=20, unique=True, serialize=False, primary_key=True),
        ),
    ]
