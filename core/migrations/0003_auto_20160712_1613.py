# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-12 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_publicroom_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicroom',
            name='created_by',
            field=models.TextField(),
        ),
    ]
