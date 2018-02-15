# -*- coding: utf-8 -*-

#######################################################################
# bPortal is a SuiteCRM portal written using django project.

# Copyright (C) 2017 Marc Sanchez Fauste
# Copyright (C) 2017 BTACTIC, SCCL

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from suitepy.suitecrm import SuiteCRM
from suitepy.bean import Bean
from .models import Layout
from .models import Role, RolePermission, RoleUser
from collections import OrderedDict
import json
from utils import *
from django.contrib.auth.decorators import login_required, permission_required
from processors import *
from django.template import RequestContext
from django.contrib.auth.models import User

# Create your views here.

@login_required
def index(request):
    template = loader.get_template('portal/index.html')
    context = basepage_processor(request)
    return HttpResponse(template.render(context, request))

@login_required
def modules(request):
    modules = SuiteCRM().get_available_modules()
    template = loader.get_template('portal/modules.html')
    context = basepage_processor(request)
    context.update({
        'modules' : modules['modules']
    })
    return HttpResponse(template.render(context, request))

@login_required
@permission_required('is_superuser')
def edit_layouts(request):
    modules = SuiteCRM().get_available_modules()
    template = loader.get_template('portal/edit_layouts.html')
    context = basepage_processor(request)
    context.update({
        'available_modules' : modules['modules']
    })
    return HttpResponse(template.render(context, request))

@login_required
def module_list(request, module):
    if user_can_read_module(request.user, module):
        if request.method == 'POST':
            records = retrieve_list_view_records(
                module,
                request.POST,
                request.user
            )
        else:
            records = retrieve_list_view_records(
                module,
                request.GET,
                request.user
            )
        template = loader.get_template('portal/module_list.html')
        context = basepage_processor(request)
        context.update(records)
    else:
        template = loader.get_template('portal/insufficient_permissions.html')
        context = basepage_processor(request)
    return HttpResponse(template.render(context, request))

@login_required
def module_detail(request, module, id):
    context = basepage_processor(request)
    record = None
    ordered_module_fields = []
    if user_can_read_module(request.user, module):
        template = loader.get_template('portal/module_detail.html')
        try:
            view = Layout.objects.get(module=module, view='detail')
            fields_detail = json.loads(view.fields)
            module_fields = SuiteCRM().get_module_fields(module)['module_fields']
            remove_colon_of_field_labels(module_fields)
            for row in fields_detail:
                row_fields = []
                for field in row:
                    if field in module_fields:
                        row_fields.append(module_fields[field])
                    elif not field:
                        row_fields.append(None)
                ordered_module_fields.append(row_fields)
            record = SuiteCRM().get_bean(module, id)
        except:
            pass
        context.update({
            'module_key' : module,
            'module_fields' : ordered_module_fields,
            'record' : record
        })
    else:
        template = loader.get_template('portal/insufficient_permissions.html')
    return HttpResponse(template.render(context, request))

@login_required
@permission_required('is_superuser')
def edit_list_layout(request, module):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        try:
            selected_fields = post_data['selected_fields']
        except KeyError:
            return JsonResponse({
                "status" : "Error",
                "error" : "Please specify 'selected_fields'."
            }, status = 400)
        view = None
        try:
            view = Layout.objects.get(module=module, view='list')
        except:
            view = Layout(module=module, view='list')
        view.fields = json.dumps(selected_fields)
        view.save()
        return JsonResponse({"status" : "Success"})
    elif request.method == 'GET':
        available_fields = get_allowed_module_fields(module)
        module_fields = OrderedDict()
        template = loader.get_template('portal/edit_list_layout.html')
        try:
            view = Layout.objects.get(module=module, view='list')
            for field in json.loads(view.fields):
                if field in available_fields:
                    module_fields[field] = available_fields[field]
                    del available_fields[field]
        except:
            pass
        context = basepage_processor(request)
        context.update({
            'module_key' : module,
            'module_fields' : module_fields,
            'available_fields' : available_fields
        })
        return HttpResponse(template.render(context, request))

@login_required
@permission_required('is_superuser')
def edit_detail_layout(request, module):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        try:
            selected_fields = post_data['selected_fields']
        except KeyError:
            return JsonResponse({
                "status" : "Error",
                "error" : "Please specify 'selected_fields'."
            }, status = 400)
        view = None
        try:
            view = Layout.objects.get(module=module, view='detail')
        except:
            view = Layout(module=module, view='detail')
        view.fields = json.dumps(selected_fields)
        view.save()
        return JsonResponse({"status" : "Success"})
    elif request.method == 'GET':
        available_fields = get_allowed_module_fields(module)
        module_fields = list()
        template = loader.get_template('portal/edit_detail_layout.html')
        try:
            view = Layout.objects.get(module=module, view='detail')
            for row in json.loads(view.fields):
                module_fields_row = []
                for field in row:
                    if field in available_fields:
                        module_fields_row.append(available_fields[field])
                        del available_fields[field]
                    elif not field:
                        module_fields_row.append(None)
                module_fields.append(module_fields_row)
        except:
            pass
        context = basepage_processor(request)
        context.update({
            'module_key' : module,
            'module_fields' : module_fields,
            'available_fields' : available_fields
        })
        return HttpResponse(template.render(context, request))

@login_required
@permission_required('is_superuser')
def edit_role(request, role):
    if request.method == 'GET':
        role_bean = None
        try:
            role_bean = Role.objects.get(name=role)
        except:
            pass
        available_modules = SuiteCRM().get_available_modules()
        module_labels = {}
        for available_module in available_modules['modules']:
            module_labels[available_module['module_key']] = \
                available_module['module_label']
        role_permissions = RolePermission.objects.filter(role=role, grant=1)
        modules_order = role_permissions.values_list('module').distinct()
        module_permissions = OrderedDict()
        for module in modules_order:
            module_key = module[0]
            if module_key in module_labels:
                module_permissions[module_key] = {
                    'module_label' : module_labels[module_key],
                    'read' : False,
                    'create' : False,
                    'edit' : False,
                    'delete' : False
                }
                del module_labels[module_key]
        for role_permission in role_permissions:
            module = role_permission.module
            action = role_permission.action
            if module in module_permissions:
                module_permissions[module][action] = True
        for module_key in module_labels:
            module_permissions[module_key] = {
                'module_label' : module_labels[module_key],
                'read' : False,
                'create' : False,
                'edit' : False,
                'delete' : False
            }
        template = loader.get_template('portal/edit_role.html')
        context = basepage_processor(request)
        context.update({
            'module_permissions' : module_permissions,
            'role' : role,
            'role_bean' : role_bean
        })
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        role_bean = None
        try:
            permissions = post_data['permissions']
        except KeyError:
            return JsonResponse({
                "status" : "Error",
                "error" : "Please specify 'permissions'."
            }, status = 400)
        try:
            role_bean = Role.objects.get(name=role)
        except:
            return JsonResponse({
                "status" : "Error",
                "error" : "Role '" + role + "' does not exist."
            }, status = 400)
        RolePermission.objects.filter(role=role).delete()
        for i, permission in enumerate(permissions):
            if permission[2]:
                RolePermission(
                    role=role_bean,
                    module=permission[0],
                    action=permission[1],
                    grant=permission[2],
                    order=i
                ).save()
        return JsonResponse({"status" : "Success"})

def crm_entry_point(request):
    if request.GET['option'] and request.GET['task'] and request.GET['sug']:
        contact = None
        try:
            contact = SuiteCRM().get_bean(
                'Contacts',
                request.GET['sug'],
                ['id', 'first_name', 'last_name', 'email1', 'account_id']
            )
        except:
            return JsonResponse({
                "status" : "Error",
                "error" : "Error retrieving contact"
            }, status = 400)
        if not contact['email1']:
            return JsonResponse({
                "status" : "Error",
                "error" : "Contact has no valid email"
            }, status = 400)
        if request.GET['task'] == 'create':
            return create_portal_user(contact)
        elif request.GET['task'] == 'disable_user':
            return disable_portal_user(contact)
        elif request.GET['task'] == 'enable_user':
            return enable_portal_user(contact)
        print request.GET['task']
    return JsonResponse({
        "status" : "Error",
        "error" : "Invalid request"
    }, status = 400)
