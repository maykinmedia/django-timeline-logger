# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-24 10:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("timeline_logger", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="timelinelog",
            options={
                "verbose_name": "timeline log entry",
                "verbose_name_plural": "timeline log entries",
            },
        ),
    ]
