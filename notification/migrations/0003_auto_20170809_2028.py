# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-09 20:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_auto_20170809_1830'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partnersitetelegram',
            old_name='telegram_user',
            new_name='chat_id',
        ),
    ]
