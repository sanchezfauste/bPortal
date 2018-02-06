# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Layout, Role, RolePermission, RoleUser, UserAttr

# Register your models here.

admin.site.register(Layout)
admin.site.register(Role)
admin.site.register(RolePermission)
admin.site.register(RoleUser)
admin.site.register(UserAttr)
