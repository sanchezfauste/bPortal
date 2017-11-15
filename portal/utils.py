#######################################################################
# Suite PY is a simple Python client for SuiteCRM API.

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

from .models import RolePermission
from collections import OrderedDict
import urllib

def remove_colon_of_field_labels(module_fields):
    for field in module_fields:
        label = module_fields[field]['label']
        if len(label) > 0 and label[-1] == ':':
            module_fields[field]['label'] = label[:-1]

def get_user_accesible_modules(user):
    try:
        role_permissions = RolePermission.objects.filter(
            role=user.roleuser.role,
            grant=True,
            action="read"
        )
        modules = OrderedDict()
        for role_permission in role_permissions:
            module_key = role_permission.module
            modules[module_key] = {
                "module_key" : module_key,
                "module_label" : module_key
            }
        return modules
    except:
        return OrderedDict()

def user_can_read_module(user, module):
    return _user_can_perform_action_on_module(user, "read", module)

def user_can_create_module(user, module):
    return _user_can_perform_action_on_module(user, "create", module)

def user_can_edit_module(user, module):
    return _user_can_perform_action_on_module(user, "edit", module)

def user_can_delete_module(user, module):
    return _user_can_perform_action_on_module(user, "delete", module)

def _user_can_perform_action_on_module(user, action, module):
    try:
        return RolePermission.objects.filter(
            role=user.roleuser.role,
            module=module,
            grant=True,
            action=action
        ).exists()
    except:
        return False

def get_filter_query(module, fields, parameters):
    table = module.lower()
    query = ''
    for field_name, field_def in fields.items():
        if field_name in parameters:
            field_table = table if field_name[-2:] != '_c' else table + '_cstm'
            field_type = field_def['type']
            if field_type in ['double', 'float', 'decimal', 'int', 'bool']:
                value = parameters[field_name]
            else:
                value = '\'' + parameters[field_name] + '\''
            if query:
                query += " AND "
            query += field_table + '.' + field_name + ' = ' + value
    return query

def get_listview_filter_urlencoded(parameters):
    filters = parameters.copy()
    if 'limit' in filters:
        del filters['limit']
    if 'offset' in filters:
        del filters['offset']
    if 'order_by' in filters:
        del filters['order_by']
    if 'order' in filters:
        del filters['order']
    return urllib.urlencode(filters)

NON_SORTABLE_FIELD_TYPES=[
    'html',
    'text',
    'encrypt'
]
NON_SORTABLE_FIELD_NAMES=[
    'email1',
    'email2',
    'parent_name'
]

def set_sortable_atribute_on_module_fields(module_fields):
    for field_name, field_def in module_fields.items():
        if field_def['type'] in NON_SORTABLE_FIELD_TYPES\
                or field_name in NON_SORTABLE_FIELD_NAMES:
            field_def['sortable'] = False
        else:
            field_def['sortable'] = True
