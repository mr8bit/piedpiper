# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-09 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='url',
            field=models.CharField(max_length=300, verbose_name='Url сайта'),
        ),
    ]