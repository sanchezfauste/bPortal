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
from .models import Layout
from suitepy.suitecrm import SuiteCRM
from collections import OrderedDict
import urllib
import json

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
        if field_name in parameters and parameters[field_name]:
            field_table = table if field_name[-2:] != '_c' else table + '_cstm'
            field_type = field_def['type']
            if field_type in ['date', 'datetime', 'datetimecombo']:
                date_filter = get_datetime_option_in_mysql_format(
                    parameters[field_name],
                    field_table + '.' + field_name
                )
                if date_filter:
                    if query:
                        query += " AND "
                    query += date_filter
            else:
                if field_type in ['double', 'float', 'decimal', 'int', 'bool']:
                    value = parameters[field_name]
                else:
                    value = '\'' + parameters[field_name] + '\''
                if query:
                    query += " AND "
                query += field_table + '.' + field_name + ' = ' + value
    return query

def get_listview_filter(parameters):
    filters = parameters.copy()
    if 'limit' in filters:
        del filters['limit']
    if 'offset' in filters:
        del filters['offset']
    if 'order_by' in filters:
        del filters['order_by']
    if 'order' in filters:
        del filters['order']
    if 'csrfmiddlewaretoken' in filters:
        del filters['csrfmiddlewaretoken']
    for key, value in filters.items():
        if not value:
            del filters[key]
    return filters

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

def retrieve_list_view_records(module, arguments):
    records = []
    module_fields = {}
    ordered_module_fields = OrderedDict()
    limit = arguments.get('limit')
    if limit:
        limit = int(limit)
    else:
        limit = 10
    offset = arguments.get('offset')
    if offset:
        offset = int(offset)
    order_by = arguments.get('order_by')
    order = arguments.get('order')
    try:
        view = Layout.objects.get(module=module, view='list')
        fields_list = json.loads(view.fields)
        module_fields = SuiteCRM().get_module_fields(module, fields_list)['module_fields']
        for field in fields_list:
            if field in module_fields:
                ordered_module_fields[field] = module_fields[field]
        remove_colon_of_field_labels(module_fields)
        set_sortable_atribute_on_module_fields(module_fields)
        order_by_string = None
        if order_by in fields_list and module_fields[order_by]['sortable']:
            order_by_string = order_by
        else:
            order_by = None
        if order_by and order in ['asc', 'desc']:
            order_by_string += ' ' + order
        else:
            order = None
        records = SuiteCRM().get_bean_list(
            module,
            max_results = limit,
            offset = offset,
            order_by = order_by_string,
            query = get_filter_query(module, module_fields, arguments)
        )
    except:
        pass

    return {
        'module_key' : module,
        'records' : records,
        'module_fields' : ordered_module_fields,
        'current_filters' : get_listview_filter(arguments),
        'order_by' : order_by,
        'order' : order
    }

def get_datetime_option_in_mysql_format(option, field_name, params = []):
    if option == '=':
        return 'DATE(' + field_name + ') = DATE(' + params[0] + ')'
    if option == 'not_equal':
        return 'DATE(' + field_name + ') != DATE(' + params[0] + ')'
    if option == 'greater_than':
        return 'DATE(' + field_name + ') > DATE(' + params[0] + ')'
    if option == 'less_than':
        return 'DATE(' + field_name + ') < DATE(' + params[0] + ')'
    if option == 'between':
        return 'DATE(' + field_name + ') BETWEEN DATE(' + params[0] \
            + ') AND DATE(' + params[1] + ')'
    if option == 'last_7_days':
        return 'DATE(' + field_name + ') >= DATE_ADD(UTC_DATE(), INTERVAL - 6 DAY)' \
                + ' AND ' + 'DATE(' + field_name + ') <= UTC_DATE()'
    if option == 'next_7_days':
        return 'DATE(' + field_name + ') >= UTC_DATE() ' \
                + ' AND ' + 'DATE(' + field_name + ') <= DATE_ADD(UTC_DATE(), INTERVAL + 6 DAY)'
    if option == 'last_30_days':
        return 'DATE(' + field_name + ') >= DATE_ADD(UTC_DATE(), INTERVAL - 29 DAY)' \
                + ' AND ' + 'DATE(' + field_name + ') <= UTC_DATE()'
    if option == 'next_30_days':
        return 'DATE(' + field_name + ') >= UTC_DATE() ' \
                + ' AND ' + 'DATE(' + field_name + ') <= DATE_ADD(UTC_DATE(), INTERVAL + 29 DAY)'
    if option == 'last_month':
        return 'YEAR(' + field_name \
                + ') = YEAR(DATE_ADD(UTC_DATE(), INTERVAL - 1 MONTH)) ' \
                + 'AND MONTH(' + field_name \
                + ') = MONTH(DATE_ADD(UTC_DATE(), INTERVAL - 1 MONTH))'
    if option == 'this_month':
        return 'YEAR(' + field_name + ') = YEAR(UTC_DATE()) AND MONTH(' \
                + field_name + ') = MONTH(UTC_DATE())'
    if option == 'next_month':
        return 'YEAR(' + field_name \
                + ') = YEAR(DATE_ADD(UTC_DATE(), INTERVAL + 1 MONTH)) ' \
                + 'AND MONTH(' + field_name \
                + ') = MONTH(DATE_ADD(UTC_DATE(), INTERVAL + 1 MONTH))'
    if option == 'last_year':
        return 'YEAR(' + field_name \
                + ') = YEAR(DATE_ADD(UTC_DATE(), INTERVAL - 1 YEAR))'
    if option == 'this_year':
        return 'YEAR(' + field_name \
                + ') = YEAR(UTC_DATE())'
    if option == 'next_year':
        return 'YEAR(' + field_name \
                + ') = YEAR(DATE_ADD(UTC_DATE(), INTERVAL + 1 YEAR))'
    return None
