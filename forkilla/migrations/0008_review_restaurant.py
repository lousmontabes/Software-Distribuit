# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-05-29 16:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forkilla', '0007_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='restaurant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='forkilla.Restaurant'),
            preserve_default=False,
        ),
    ]