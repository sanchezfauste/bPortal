# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-05-14 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_auto_20180503_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layout',
            name='view',
            field=models.CharField(choices=[('list', 'List View'), ('filter', 'Filter View'), ('detail', 'Detail View'), ('edit', 'Edit View'), ('create', 'Create View')], max_length=30),
        ),
    ]