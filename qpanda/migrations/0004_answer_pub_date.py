# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('qpanda', '0003_auto_20160212_0332'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 13, 6, 53, 56, 359834, tzinfo=utc), verbose_name=b'date published'),
            preserve_default=False,
        ),
    ]
