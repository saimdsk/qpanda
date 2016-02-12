# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qpanda', '0002_auto_20160206_0147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_text', models.TextField(verbose_name=b'Answer')),
                ('question', models.ForeignKey(to='qpanda.Question')),
            ],
        ),
        migrations.RemoveField(
            model_name='pollchoice',
            name='question',
        ),
        migrations.DeleteModel(
            name='PollChoice',
        ),
    ]
