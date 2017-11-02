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
from .models import Layout
from collections import OrderedDict
import json
from utils import *
from django.contrib.auth.decorators import login_required
from processors import *
from django.template import RequestContext

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
def module_list(request, module):
    records = []
    module_fields = {}
    limit = request.GET.get('limit')
    if limit:
        limit = int(limit)
    else:
        limit = 10
    offset = request.GET.get('offset')
    if offset:
        offset = int(offset)
    try:
        view = Layout.objects.get(module=module, view='list')
        fields_list = json.loads(view.fields)
        module_fields = SuiteCRM().get_module_fields(module, fields_list)['module_fields']
        remove_colon_of_field_labels(module_fields)
        records = SuiteCRM().get_bean_list(module, max_results = limit, offset = offset)
    except:
        pass
    template = loader.get_template('portal/module_list.html')
    context = basepage_processor(request)
    context.update({
        'module_key' : module,
        'records' : records,
        'module_fields' : module_fields
    })
    return HttpResponse(template.render(context, request))

@login_required
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
        available_fields = SuiteCRM().get_module_fields(module)['module_fields']
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
def edit_role(request, role):
    if request.method == 'GET':
        available_modules = SuiteCRM().get_available_modules()
        template = loader.get_template('portal/edit_role.html')
        context = basepage_processor(request)
        context.update({
            'available_modules' : available_modules['modules'],
            'role' : role
        })
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        import sys
        sys.stdout.write('Receiving role: %s\n%s' % (role, json.dumps(post_data)))
        return JsonResponse({"status" : "Success"})
