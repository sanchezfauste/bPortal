# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Layout(models.Model):

    module = models.CharField(max_length=50)
    VIEW_CHOICES = (
        ('list', 'List View'),
        ('edit', 'Edit View'),
        ('create', 'Create View'),
    )
    view = models.CharField(max_length=30, choices=VIEW_CHOICES)
    fields = models.TextField()

    class Meta:
        unique_together = ("module", "view")

    def __str__(self):
        return self.module + ' - ' + self.view + ' view'
