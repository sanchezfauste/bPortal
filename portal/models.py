# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Layout(models.Model):

    module = models.CharField(max_length=50)
    VIEW_CHOICES = (
        ('list', _('List View')),
        ('filter', _('Filter View')),
        ('detail', _('Detail View')),
        ('edit', _('Edit View')),
        ('create', _('Create View')),
    )
    view = models.CharField(max_length=30, choices=VIEW_CHOICES)
    fields = models.TextField()

    class Meta:
        unique_together = ("module", "view")

    def __str__(self):
        return self.module + ' - ' + self.view + ' view'


class Role(models.Model):

    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class RolePermission(models.Model):

    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    module = models.CharField(max_length=50)
    ACTION_CHOICES = (
        ('read', _('Read')),
        ('create', _('Create')),
        ('edit', _('Edit')),
        ('delete', _('Delete')),
    )
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    grant = models.BooleanField()
    order = models.IntegerField()

    class Meta:
        unique_together = ("role", "module", "action")
        ordering = ['order']

    def __str__(self):
        return self.role.name + ' - ' + self.action.title() + ' ' + self.module


class RoleUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)

    def __str__(self):
        return self.role.name + ' - ' + self.user.username


class UserAttr(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_id = models.CharField(max_length=36)
    account_id = models.CharField(max_length=36)
    USER_TYPE_CHOISES = (
        ('single', _('Single')),
        ('account', _('Account'))
    )
    user_type = models.CharField(
        max_length=30,
        choices=USER_TYPE_CHOISES,
        default='single'
    )

    def __str__(self):
        return self.user.username


class PortalSetting(models.Model):

    name = models.CharField(max_length=100, primary_key=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' : ' + self.value
