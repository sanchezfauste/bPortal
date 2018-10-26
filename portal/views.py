# -*- coding: utf-8 -*-

#######################################################################
# bPortal is a SuiteCRM portal written using django project.

# Copyright (C) 2017-2018 BTACTIC, SCCL
# Copyright (C) 2017-2018 Marc Sanchez Fauste

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
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from suitepy.suitecrm import SuiteCRM
from suitepy.suitecrm_cached import SuiteCRMCached
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
from django.utils.translation import gettext as _
from cases import *
from aos_quotes_utils import *
from pdf_templates import *
import mimetypes
import base64
from django.http import Http404
from django.urls import reverse

# Create your views here.


@login_required
def index(request):
    template = loader.get_template('portal/index.html')
    context = basepage_processor(request)
    return HttpResponse(template.render(context, request))


@login_required
def modules(request):
    modules = get_available_modules()
    template = loader.get_template('portal/modules.html')
    context = basepage_processor(request)
    context.update({
        'modules': modules
    })
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('is_superuser')
def edit_layouts(request):
    modules = get_available_modules()
    template = loader.get_template('portal/edit_layouts.html')
    context = basepage_processor(request)
    context.update({
        'available_modules': modules
    })
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('is_superuser')
def edit_roles_generic(request, context={}):
    template = loader.get_template('portal/edit_roles.html')
    context.update(basepage_processor(request))
    context.update({
        'roles': Role.objects.all(),
        'default_role': get_default_role()
    })
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('is_superuser')
def edit_users(request):
    template = loader.get_template('portal/edit_users.html')
    context = basepage_processor(request)
    context.update({
        'users': User.objects.all()
    })
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('is_superuser')
def edit_user(request, user_id):
    context = basepage_processor(request)
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user_id)
            role = Role.objects.get(name=request.POST['user_role'])
            try:
                user.roleuser.role = role
                user.roleuser.save()
            except Exception:
                RoleUser(
                    user=user,
                    role=role
                ).save()
            try:
                user.userattr.user_type = request.POST['user_type']
                user.userattr.save()
            except Exception:
                UserAttr(
                    user=user,
                    user_type=request.POST['user_type']
                ).save()
            context.update({
                'success_msg': True,
                'msg': _('User settings updated successfully.')
            })
        except Exception:
            context.update({
                'error_msg': True,
                'msg': _('Error while saving user settings.')
            })
    template = loader.get_template('portal/edit_user.html')
    context.update({
        'user': User.objects.get(id=user_id),
        'roles': Role.objects.all(),
        'user_types': UserAttr.USER_TYPE_CHOISES
    })
    return HttpResponse(template.render(context, request))


@login_required
def user_profile(request):
    context = basepage_processor(request)
    template = loader.get_template('portal/user_profile.html')
    context.update({
        'user': request.user
    })
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('is_superuser')
def edit_roles(request):
    return edit_roles_generic(request)


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
        context.update({
            'user_can_edit': user_can_edit_module(request.user, module),
            'user_can_delete': user_can_delete_module(request.user, module),
            'user_can_create': user_can_create_module(request.user, module)
        })
    else:
        template = loader.get_template('portal/insufficient_permissions.html')
        context = basepage_processor(request)
    return HttpResponse(template.render(context, request))


@login_required
def user_records(request, module):
    records = get_related_user_records(module, request.user)
    records_json = {
        'records': []
    }
    if records and 'entry_list' in records:
        for record in records['entry_list']:
            records_json['records'].append(record.json)
    return JsonResponse(records_json)


@login_required
def module_detail(request, module, id):
    context = basepage_processor(request)
    record = None
    ordered_module_fields = get_module_view_fields(module, 'detail')
    if user_can_read_module(request.user, module) and user_can_read_record(request.user, module, id):
        template = loader.get_template('portal/module_detail.html')
        try:
            if module == 'Cases':
                record = get_case(id)
                context.update({
                    'case_updates': get_case_updates(id)
                })
            elif module == 'AOS_Invoices' or module == 'AOS_Quotes' or module == 'AOS_Contracts':
                record = get_aos_quotes_record(module, id)
                context.update({
                    'pdf_template_enabled': True if get_pdf_template_id(module) else None
                })
            else:
                record = SuiteCRM().get_bean(module, id)
        except Exception:
            pass
        context.update({
            'module_key': module,
            'module_fields': ordered_module_fields,
            'record': record,
            'user_can_edit': user_can_edit_module(request.user, module),
            'user_can_delete': user_can_delete_module(request.user, module)
        })
    else:
        template = loader.get_template('portal/insufficient_permissions.html')
    return HttpResponse(template.render(context, request))


@login_required
def module_remove_record(request, module):
    if request.method == 'POST' and 'id' in request.POST:
        id = request.POST['id']
        if user_can_delete_module(request.user, module) \
                and user_is_linked_to_record(request.user, module, id):
            bean = Bean(module)
            bean['id'] = id
            bean['deleted'] = 1
            try:
                SuiteCRM().save_bean(bean)
                return JsonResponse({
                    "status": "Success",
                    "msg": _("Record deleted successfully.")
                })
            except Exception as e:
                return JsonResponse(
                    {
                        "status": "Error",
                        "error": _("Error deleting record.")
                    },
                    status=400
                )
        else:
            return JsonResponse(
                {
                    "status": "Error",
                    "error": _("Insufficient permissions.")
                },
                status=400
            )
    return JsonResponse(
        {
            "status": "Error",
            "error": _("Invalid request.")
        },
        status=400
    )


def create_case_add_attachments(request, bean_case):
    try:
        files = request.FILES.getlist('update-case-attachment')
        if files:
            case_update = Bean('AOP_Case_Updates')
            case_update['contact_id'] = request.user.userattr.contact_id
            case_update['case_id'] = bean_case['id']
            case_update['name'] = bean_case['description'][:45]
            case_update['description'] = bean_case['description'].replace('\n', '<br>')
            case_update['internal'] = 0
            SuiteCRM().save_bean(case_update)
            if case_update['id']:
                for f in files:
                    note = Bean('Notes')
                    note['name'] = f.name
                    note['parent_type'] = 'AOP_Case_Updates'
                    note['parent_id'] = case_update['id']
                    note['contact_id'] = request.user.userattr.contact_id
                    SuiteCRM().save_bean(note)
                    if note['id']:
                        SuiteCRM().set_note_attachment(
                            note['id'],
                            f.name,
                            base64.b64encode(f.read())
                        )
                return True
    except Exception:
        pass
    return False


@login_required
def module_create(request, module):
    context = basepage_processor(request)
    ordered_module_fields = get_module_view_fields(module, 'create')
    if user_can_create_module(request.user, module):
        template = loader.get_template('portal/module_create.html')
        if request.method == 'POST':
            try:
                bean = get_bean_from_post(module, 'create', request.POST)
                try:
                    module_def = ModuleDefinitionFactory.get_module_definition(module)
                    module_def.before_save_on_create_hook(bean, request)
                except Exception:
                    pass
                SuiteCRM().save_bean(bean)
                relate_result = relate_bean_with_user(bean, request.user)
                context.update(relate_result)
                context.update({
                    'record_created_successfully': True
                })
                if module == 'Cases':
                    create_case_add_attachments(request, bean)
                url = reverse(
                    'module_detail',
                    kwargs={
                        'module': module,
                        'id': bean['id']
                    }
                )
                return HttpResponseRedirect(url)
            except Exception as e:
                print e
                context.update({
                    'error_on_create': True
                })
        context.update({
            'module_key': module,
            'module_fields': ordered_module_fields
        })
    else:
        template = loader.get_template('portal/insufficient_permissions.html')
    return HttpResponse(template.render(context, request))


@login_required
def module_edit(request, module, id):
    context = basepage_processor(request)
    record = None
    ordered_module_fields = get_module_view_fields(module, 'edit')
    if user_can_edit_module(request.user, module) and user_is_linked_to_record(request.user, module, id):
        template = loader.get_template('portal/module_edit.html')
        if request.method == 'POST':
            try:
                bean = get_bean_from_post(module, 'edit', request.POST)
                bean['id'] = id
                try:
                    module_def = ModuleDefinitionFactory.get_module_definition(module)
                    module_def.before_save_on_edit_hook(bean, request)
                except Exception:
                    pass
                SuiteCRM().save_bean(bean)
                context.update({
                    'record_edited': True
                })
                url = reverse(
                    'module_detail',
                    kwargs={
                        'module': module,
                        'id': id
                    }
                )
                return HttpResponseRedirect(url)
            except Exception:
                context.update({
                    'error_on_save': True
                })
        try:
            record = SuiteCRM().get_bean(module, id)
        except Exception:
            context.update({
                'error_retrieving_bean': True
            })
        context.update({
            'module_key': module,
            'module_fields': ordered_module_fields,
            'record': record
        })
    else:
        template = loader.get_template('portal/insufficient_permissions.html')
    return HttpResponse(template.render(context, request))


@login_required
def close_case(request):
    if user_can_read_module(request.user, 'Cases') and request.method == 'POST' \
            and 'case-id' in request.POST \
            and user_is_linked_to_case(request.user, request.POST['case-id']):
        try:
            bean = Bean('Cases')
            bean['id'] = request.POST['case-id']
            bean['state'] = 'Closed'
            bean['status'] = 'Closed_Closed'
            SuiteCRM().save_bean(bean)
        except Exception:
            pass
        url = reverse(
            'module_detail',
            kwargs={
                'module': 'Cases',
                'id': request.POST['case-id']
            }
        )
        return HttpResponseRedirect(url)
    else:
        context = basepage_processor(request)
        template = loader.get_template('portal/insufficient_permissions.html')
        return HttpResponse(template.render(context, request))


@login_required
def reopen_case(request):
    if user_can_read_module(request.user, 'Cases') and request.method == 'POST' \
            and 'case-id' in request.POST \
            and user_is_linked_to_case(request.user, request.POST['case-id']):
        try:
            bean = Bean('Cases')
            bean['id'] = request.POST['case-id']
            bean['state'] = 'Open'
            bean['status'] = 'Open_New'
            SuiteCRM().save_bean(bean)
        except Exception:
            pass
        url = reverse(
            'module_detail',
            kwargs={
                'module': 'Cases',
                'id': request.POST['case-id']
            }
        )
        return HttpResponseRedirect(url)
    else:
        context = basepage_processor(request)
        template = loader.get_template('portal/insufficient_permissions.html')
        return HttpResponse(template.render(context, request))


@login_required
def add_case_update(request):
    if user_can_read_module(request.user, 'Cases') and request.method == 'POST':
        if request.method == 'POST' and 'case-id' in request.POST \
                and 'update-case-text' in request.POST \
                and user_is_linked_to_case(request.user, request.POST['case-id']):
            update_case_text = request.POST['update-case-text'].strip()
            if not update_case_text:
                return JsonResponse(
                    {
                        "status": "Error",
                        "error": _("Empty case updates are not allowed.")
                    },
                    status=400
                )
            case_update = Bean('AOP_Case_Updates')
            case_update['contact_id'] = request.user.userattr.contact_id
            case_update['case_id'] = request.POST['case-id']
            case_update['name'] = update_case_text[:45]
            case_update['description'] = update_case_text
            case_update['internal'] = 0
            try:
                SuiteCRM().save_bean(case_update)
                if case_update['id']:
                    for f in request.FILES.getlist('update-case-attachment'):
                        note = Bean('Notes')
                        note['name'] = f.name
                        note['parent_type'] = 'AOP_Case_Updates'
                        note['parent_id'] = case_update['id']
                        note['contact_id'] = request.user.userattr.contact_id
                        SuiteCRM().save_bean(note)
                        if note['id']:
                            SuiteCRM().set_note_attachment(
                                note['id'],
                                f.name,
                                base64.b64encode(f.read())
                            )
                        else:
                            return JsonResponse(
                                {
                                    "status": "Error",
                                    "error": _("An error occurred while uploading the attachment(s).")
                                },
                                status=400
                            )
                else:
                    return JsonResponse(
                        {
                            "status": "Error",
                            "error": _("An error occurred while creating the case update.")
                        },
                        status=400
                    )
                return JsonResponse({
                    "status": "Success",
                    "msg": _("The case update has been added successfully."),
                    "case_update": render_to_string(
                        'portal/module_detail_case_update.html',
                        {
                            "update": get_case_update(case_update['id']),
                            "show": True
                        }
                    )
                })
            except Exception:
                return JsonResponse(
                    {
                        "status": "Error",
                        "error": _("An error occurred while updating the case.")
                    },
                    status=400
                )
    return JsonResponse(
        {
            "status": "Error",
            "error": _("Invalid request.")
        },
        status=400
    )


@login_required
def note_attachment(request, id):
    attachment = SuiteCRM().get_note_attachment(id)['note_attachment']
    if attachment['file']:
        response = HttpResponse(
            base64.b64decode(attachment['file']),
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = "attachment; filename=%s" \
            % attachment['filename']
        return response
    else:
        raise Http404(_("The requested file was not found."))


@login_required
@permission_required('is_superuser')
def edit_list_layout(request, module):
    return list_layout(request, module, 'list')


@login_required
@permission_required('is_superuser')
def edit_filter_layout(request, module):
    return list_layout(request, module, 'filter')


def list_layout(request, module, layout):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        try:
            selected_fields = post_data['selected_fields']
        except KeyError:
            return JsonResponse(
                {
                    "status": "Error",
                    "error": _("Please specify 'selected_fields'.")
                },
                status=400
            )
        view = None
        try:
            view = Layout.objects.get(module=module, view=layout)
        except Exception:
            view = Layout(module=module, view=layout)
        view.fields = json.dumps(selected_fields)
        view.save()
        return JsonResponse({
            "status": "Success",
            "msg": _("Layout updated successfully")
        })
    elif request.method == 'GET':
        if layout == 'filter':
            available_fields = get_filterable_fields(module)
        else:
            available_fields = get_allowed_module_fields(module)
        module_fields = OrderedDict()
        template = loader.get_template('portal/edit_list_layout.html')
        try:
            view = Layout.objects.get(module=module, view=layout)
            for field in json.loads(view.fields):
                if field in available_fields:
                    module_fields[field] = available_fields[field]
                    del available_fields[field]
        except Exception:
            pass
        context = basepage_processor(request)
        context.update({
            'module_key': module,
            'module_fields': module_fields,
            'available_fields': available_fields,
            'layout': layout
        })
        return HttpResponse(template.render(context, request))


@login_required
@permission_required('is_superuser')
def edit_detail_layout(request, module):
    return edit_layout(request, module, 'detail')


@login_required
@permission_required('is_superuser')
def edit_edit_layout(request, module):
    return edit_layout(request, module, 'edit')


@login_required
@permission_required('is_superuser')
def edit_create_layout(request, module):
    return edit_layout(request, module, 'create')


def edit_layout(request, module, layout):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        try:
            selected_fields = post_data['selected_fields']
        except KeyError:
            return JsonResponse(
                {
                    "status": "Error",
                    "error": _("Please specify 'selected_fields'.")
                },
                status=400
            )
        view = None
        try:
            view = Layout.objects.get(module=module, view=layout)
        except Exception:
            view = Layout(module=module, view=layout)
        view.fields = json.dumps(selected_fields)
        view.save()
        return JsonResponse({
            "status": "Success",
            "msg": _("Layout updated successfully")
        })
    elif request.method == 'GET':
        available_fields = get_allowed_module_fields(module)
        module_fields = list()
        template = loader.get_template('portal/edit_layout.html')
        try:
            view = Layout.objects.get(module=module, view=layout)
            for row in json.loads(view.fields):
                module_fields_row = []
                for field in row:
                    if field in available_fields:
                        module_fields_row.append(available_fields[field])
                        del available_fields[field]
                    elif not field:
                        module_fields_row.append(None)
                module_fields.append(module_fields_row)
        except Exception:
            pass
        context = basepage_processor(request)
        context.update({
            'module_key': module,
            'module_fields': module_fields,
            'available_fields': available_fields,
            'layout': layout
        })
        return HttpResponse(template.render(context, request))


@login_required
@permission_required('is_superuser')
def edit_role(request, role):
    if request.method == 'GET':
        role_bean = None
        try:
            role_bean = Role.objects.get(name=role)
        except Exception:
            pass
        module_labels = get_module_labels()
        role_permissions = RolePermission.objects.filter(role=role, grant=1)
        modules_order = role_permissions.values_list('module').distinct()
        module_permissions = OrderedDict()
        for module in modules_order:
            module_key = module[0]
            if module_key in module_labels:
                module_permissions[module_key] = {
                    'module_label': module_labels[module_key],
                    'read': False,
                    'create': False,
                    'edit': False,
                    'delete': False
                }
                del module_labels[module_key]
        for role_permission in role_permissions:
            module = role_permission.module
            action = role_permission.action
            if module in module_permissions:
                module_permissions[module][action] = True
        for module_key in module_labels:
            module_permissions[module_key] = {
                'module_label': module_labels[module_key],
                'read': False,
                'create': False,
                'edit': False,
                'delete': False
            }
        template = loader.get_template('portal/edit_role.html')
        context = basepage_processor(request)
        context.update({
            'module_permissions': module_permissions,
            'role': role,
            'role_bean': role_bean
        })
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        role_bean = None
        try:
            permissions = post_data['permissions']
        except KeyError:
            return JsonResponse(
                {
                    "status": "Error",
                    "error": _("Please specify 'permissions'.")
                },
                status=400
            )
        try:
            role_bean = Role.objects.get(name=role)
        except Exception:
            return JsonResponse(
                {
                    "status": "Error",
                    "error": _('Role \'%(role)s\' does not exist.') % {'role': role}
                },
                status=400
            )
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
        return JsonResponse({
            "status": "Success",
            "msg": _("Role permissions have been updated.")
        })


@login_required
@permission_required('is_superuser')
def delete_role(request):
    context = {}
    if request.method == 'POST':
        try:
            role_name = request.POST['role_name']
            role = Role.objects.get(name=role_name)
            default_role = get_default_role()
            if role != default_role:
                role.delete()
                context.update({
                    'success_msg': True,
                    'msg':  _('\'%(role)s\' role has been removed.') % {'role': role_name}
                })
            else:
                context.update({
                    'error_msg': True,
                    'msg':  _('Default role can not be deleted.')
                })
        except Exception:
            context.update({
                'error_msg': True,
                'msg': _('Role \'%(role)s\' does not exist.') % {'role': role_name}
            })
    return edit_roles_generic(request, context)


@login_required
@permission_required('is_superuser')
def create_role(request):
    context = {}
    if request.method == 'POST':
        try:
            role = request.POST['role_name']
            if len(role.strip()) > 0:
                r = Role(name=role)
                r.save()
                context.update({
                    'success_msg': True,
                    'msg': _('\'%(role)s\' role has been created.') % {'role': role}
                })
            else:
                context.update({
                    'error_msg': True,
                    'msg': _('Error creating role: Invalid role name.')
                })
        except Exception:
            context.update({
                'error_msg': True,
                'msg': _('Error creating role.')
            })
    return edit_roles_generic(request, context)


def crm_entry_point(request):
    if request.GET['option'] and request.GET['task'] and request.GET['sug']:
        contact = None
        try:
            contact = SuiteCRM().get_bean(
                'Contacts',
                request.GET['sug'],
                ['id', 'first_name', 'last_name', 'email1', 'account_id']
            )
        except Exception:
            return JsonResponse(
                {
                    "status": "Error",
                    "error": _("Error retrieving contact")
                },
                status=400
            )
        if not contact['email1']:
            return JsonResponse(
                {
                    "status": "Error",
                    "error": _("Contact has no valid email")
                },
                status=400
            )
        if request.GET['task'] == 'create':
            return create_portal_user(contact)
        elif request.GET['task'] == 'disable_user':
            return disable_portal_user(contact)
        elif request.GET['task'] == 'enable_user':
            return enable_portal_user(contact)
        print request.GET['task']
    return JsonResponse(
        {
            "status": "Error",
            "error": _("Invalid request")
        },
        status=400
    )


@login_required
@permission_required('is_superuser')
def cache(request):
    context = basepage_processor(request)
    if request.method == 'POST' and 'action' in request.POST:
        if request.POST['action'] == 'clean_cache':
            SuiteCRMCached().clear_cache()
            context.update({
                'success_msg': True,
                'msg': _('The cache has been cleared.')
            })
    context.update({
        'cached_calls': SuiteCRMCached().get_number_of_cached_calls()
    })
    template = loader.get_template('portal/cache.html')
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('is_superuser')
def pdf_templates(request):
    context = basepage_processor(request)
    if request.method == 'POST' and 'action' in request.POST:
        if request.POST['action'] == 'update_preferences':
            try:
                set_pdf_template_id(
                    'AOS_Invoices',
                    request.POST['invoice_template']
                )
                set_pdf_template_id(
                    'AOS_Quotes',
                    request.POST['quote_template']
                )
                set_pdf_template_id(
                    'AOS_Contracts',
                    request.POST['contract_template']
                )
                context.update({
                    'success_msg': True,
                    'msg': _('Preferences have been updated correctly.')
                })
            except Exception:
                context.update({
                    'error_msg': True,
                    'msg': _('Error updating preferences.')
                })
    context.update({
        'aos_invoices_templates': get_aos_invoices_pdf_templates(),
        'aos_quotes_templates': get_aos_quotes_pdf_templates(),
        'aos_contract_templates': get_aos_contracts_pdf_templates(),
        'invoice_template': get_pdf_template_id('AOS_Invoices'),
        'quote_template': get_pdf_template_id('AOS_Quotes'),
        'contract_template': get_pdf_template_id('AOS_Contracts')
    })
    template = loader.get_template('portal/pdf_templates.html')
    return HttpResponse(template.render(context, request))


@login_required
def get_pdf(request, module, id):
    context = basepage_processor(request)
    template_id = get_pdf_template_id(module)
    if user_can_read_module(request.user, module) \
            and user_can_read_record(request.user, module, id) \
            and template_id:
        try:
            pdf = SuiteCRM().get_pdf_template(
                template_id,
                module,
                id
            )
            if pdf['error']:
                raise Http404(_("The requested file was not found."))
            else:
                response = HttpResponse(
                    base64.b64decode(pdf['file']),
                    content_type='application/octet-stream'
                )
                response['Content-Disposition'] = "attachment; filename=%s" \
                    % pdf['filename']
                return response
        except Exception:
            context.update({
                'msg': _('Error while retrieving document.')
            })
            template = loader.get_template('portal/error.html')
            return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('portal/insufficient_permissions.html')
        return HttpResponse(template.render(context, request))
