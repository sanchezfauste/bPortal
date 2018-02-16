# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-22 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_auto_20171107_1651'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rolepermission',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='layout',
            name='view',
            field=models.CharField(choices=[('list', 'List View'), ('detail', 'Detail View'), ('edit', 'Edit View'), ('create', 'Create View')], max_length=30),
        ),
    ]