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

from .models import RolePermission
from .models import Layout
from suitepy.suitecrm import SuiteCRM
from suitepy.suitecrm_cached import SuiteCRMCached
from collections import OrderedDict
import urllib
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import UserAttr
from .models import Role, RoleUser
from suitepy.bean import Bean
from module_definitions import *
from django.conf import settings
from datetime import datetime

def remove_colon_of_field_labels(module_fields):
    for field in module_fields:
        label = module_fields[field]['label']
        if len(label) > 0 and label[-1] == ':':
            module_fields[field]['label'] = label[:-1]

def get_user_role(user):
    try:
        return user.roleuser.role
    except:
        default_role = get_default_role()
        if default_role:
            RoleUser(
                user = user,
                role = default_role
            ).save()
        return default_role

def get_user_accesible_modules(user):
    try:
        role_permissions = RolePermission.objects.filter(
            role=get_user_role(user),
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
            role=get_user_role(user),
            module=module,
            grant=True,
            action=action
        ).exists()
    except:
        return False

def get_filter_related(module, field_name, value):
    table = module.lower()
    field_table = table if field_name[-2:] != '_c' else table + '_cstm'
    return field_table + '.' + field_name + ' = \'' + value + '\''

def get_filter_parent(module, parent_type, parent_id):
    table = module.lower()
    return 'parent_type = \'' + parent_type + '\' AND parent_id = \'' + parent_id + '\''

def get_filter_query(module, fields, parameters):
    table = module.lower()
    query = ''
    for field_name, field_def in fields.items():
        if field_name in parameters and parameters[field_name]:
            field_table = table if field_name[-2:] != '_c' else table + '_cstm'
            field_type = field_def['type']
            if field_type in ['date', 'datetime', 'datetimecombo']:
                date_filter_params = []
                if field_name + '_1' in parameters:
                    date_filter_params.append(parameters[field_name + '_1'])
                    if field_name + '_2' in parameters:
                        date_filter_params.append(parameters[field_name + '_2'])
                date_filter = get_datetime_option_in_mysql_format(
                    parameters[field_name],
                    field_table + '.' + field_name,
                    date_filter_params
                )
                if date_filter:
                    if query:
                        query += " AND "
                    query += date_filter
            elif field_type == 'multienum':
                multienum_filter = get_multienum_filter_in_mysql_format(
                    field_table + '.' + field_name,
                    parameters.getlist(field_name)
                )
                if multienum_filter:
                    if query:
                        query += " AND "
                    query += multienum_filter
            elif field_type in ['text', 'varchar', 'name']:
                value = '\'%' + parameters[field_name] + '%\''
                if query:
                    query += " AND "
                query += field_table + '.' + field_name + ' like ' + value
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
    'encrypt',
    'relate'
]
NON_SORTABLE_FIELD_NAMES=[
    'email1',
    'email2',
    'parent_name'
]

NON_FILTERABLE_FIELD_TYPES=[
    'html',
    'text',
    'encrypt',
    'relate',
    'assigned_user_name',
    'id'
]
NON_FILTERABLE_FIELD_NAMES=[
    'email1',
    'email2',
    'parent_name'
]


FIELD_TYPES_DISALLOWED_ON_VIEWS=[
    'id',
    'function'
]
FIELD_NAMES_DISALLOWED_ON_VIEWS=[
    'modified_user_id',
    'created_by',
    'deleted',
    'assigned_user_id'
]

FORBIDDEN_MODULES=[
    'Home',
    'Calendar'
]

def set_sortable_atribute_on_module_fields(module_fields):
    for field_name, field_def in module_fields.items():
        if field_def['type'] in NON_SORTABLE_FIELD_TYPES\
                or field_name in NON_SORTABLE_FIELD_NAMES:
            field_def['sortable'] = False
        else:
            field_def['sortable'] = True

def get_filterable_fields(module_fields):
    filterable_fields = OrderedDict()
    for field_name, field_def in module_fields.items():
        if field_def['type'] not in NON_FILTERABLE_FIELD_TYPES\
                and field_name not in NON_FILTERABLE_FIELD_NAMES:
            filterable_fields[field_name] = field_def
    return filterable_fields

def get_allowed_module_fields(module):
    available_fields = SuiteCRMCached().get_module_fields(module)['module_fields']
    allowed_fields = OrderedDict()
    for field_name, field_def in available_fields.items():
        if field_def['type'] not in FIELD_TYPES_DISALLOWED_ON_VIEWS\
                and field_name not in FIELD_NAMES_DISALLOWED_ON_VIEWS:
            allowed_fields[field_name] = field_def
    return allowed_fields

def retrieve_list_view_records(module, arguments, user):
    try:
        module_def = ModuleDefinitionFactory.get_module_definition(module)
    except ModuleDefinitionNotFoundException:
        return {
            'module_key' : module,
            'unsupported_module' : True
        }
    try:
        user_type = user.userattr.user_type
        if user_type == 'account':
            related_module = 'Accounts'
            related_id = user.userattr.account_id
            link_type = module_def.accounts_link_type
            link_name = module_def.accounts_link_name
        else:
            related_module = 'Contacts'
            related_id = user.userattr.contact_id
            link_type = module_def.contacts_link_type
            link_name = module_def.contacts_link_name
    except:
        return {
            'module_key' : module,
            'error_retrieving_records' : True
        }
    records = []
    module_fields = {}
    ordered_module_fields = OrderedDict()
    filterable_fields = OrderedDict()
    limit = arguments.get('limit')
    if limit:
        limit = int(limit)
    else:
        limit = 20
    offset = arguments.get('offset')
    if offset:
        offset = int(offset)
    order_by = arguments.get('order_by')
    order = arguments.get('order')
    try:
        view = Layout.objects.get(module=module, view='list')
        fields_list = json.loads(view.fields)
        module_fields = SuiteCRMCached().get_module_fields(module, fields_list)['module_fields']
        for field in fields_list:
            if field in module_fields:
                ordered_module_fields[field] = module_fields[field]
        remove_colon_of_field_labels(module_fields)
        set_sortable_atribute_on_module_fields(module_fields)
        filterable_fields = get_filterable_fields(ordered_module_fields)
        order_by_string = None
        if order_by in fields_list and module_fields[order_by]['sortable']:
            order_by_string = order_by
        else:
            order_by = None
        if order_by and order in ['asc', 'desc']:
            order_by_string += ' ' + order
        else:
            order = None
        filter_query = get_filter_query(module, filterable_fields, arguments)
        if link_type == LinkType.RELATED:
            if filter_query:
                filter_query += " AND "
            filter_query += get_filter_related(
                module,
                link_name,
                related_id
            )
            if module_def.custom_where:
                if filter_query:
                    filter_query += " AND "
                filter_query += module_def.custom_where
            records = SuiteCRM().get_bean_list(
                module,
                max_results = limit,
                offset = offset,
                order_by = order_by_string,
                query = filter_query
            )
        elif link_type == LinkType.RELATIONSHIP:
            if module_def.custom_where:
                if filter_query:
                    filter_query += " AND "
                filter_query += module_def.custom_where
            records = SuiteCRM().get_relationships(
                related_module,
                related_id,
                link_name,
                related_fields = ['id'] + fields_list,
                limit = limit,
                offset = offset,
                order_by = order_by_string,
                related_module_query = filter_query
            )
        elif link_type == LinkType.PARENT:
            if filter_query:
                filter_query += " AND "
            filter_query += get_filter_parent(
                module,
                related_module,
                related_id
            )
            if module_def.custom_where:
                if filter_query:
                    filter_query += " AND "
                filter_query += module_def.custom_where
            records = SuiteCRM().get_bean_list(
                module,
                max_results = limit,
                offset = offset,
                order_by = order_by_string,
                query = filter_query
            )
        elif link_type == LinkType.NONE:
            if module_def.custom_where:
                if filter_query:
                    filter_query += " AND "
                filter_query += module_def.custom_where
            records = SuiteCRM().get_bean_list(
                module,
                max_results = limit,
                offset = offset,
                order_by = order_by_string,
                query = filter_query
            )
    except:
        pass

    return {
        'module_key' : module,
        'records' : records,
        'module_fields' : ordered_module_fields,
        'filterable_fields' : filterable_fields,
        'current_filters' : get_listview_filter(arguments),
        'order_by' : order_by,
        'order' : order
    }

# Function used to populate dropdowns
def get_related_user_records(module, user):
    records = None
    try:
        module_def = ModuleDefinitionFactory.get_module_definition(module)
        user_type = user.userattr.user_type
        if user_type == 'account':
            related_module = 'Accounts'
            related_id = user.userattr.account_id
            link_type = module_def.accounts_link_type
            link_name = module_def.accounts_link_name
        else:
            related_module = 'Contacts'
            related_id = user.userattr.contact_id
            link_type = module_def.contacts_link_type
            link_name = module_def.contacts_link_name

        fields_list = ['id', 'name']
        order_by = 'name'
        if link_type == LinkType.RELATED:
            filter_query = get_filter_related(
                module,
                link_name,
                related_id
            )
            if module_def.custom_where:
                if filter_query:
                    filter_query += " AND "
                filter_query += module_def.custom_where
            records = SuiteCRM().get_bean_list(
                module,
                order_by = order_by,
                select_fields = fields_list,
                query = filter_query
            )
        elif link_type == LinkType.RELATIONSHIP:
            filter_query = ''
            if module_def.custom_where:
                filter_query = module_def.custom_where
            records = SuiteCRM().get_relationships(
                related_module,
                related_id,
                link_name,
                related_fields = fields_list,
                order_by = order_by,
                related_module_query = filter_query
            )
        elif link_type == LinkType.PARENT:
            filter_query = get_filter_parent(
                module,
                related_module,
                related_id
            )
            if module_def.custom_where:
                if filter_query:
                    filter_query += " AND "
                filter_query += module_def.custom_where
            records = SuiteCRM().get_bean_list(
                module,
                order_by = order_by,
                query = filter_query,
                select_fields = fields_list
            )
        elif link_type == LinkType.NONE:
            filter_query = ''
            if module_def.custom_where:
                filter_query = module_def.custom_where
            records = SuiteCRM().get_bean_list(
                module,
                order_by = order_by,
                query = filter_query,
                select_fields = fields_list
            )
    except:
        return None
    return records

def get_datetime_option_in_mysql_format(option, field_name, params = []):
    if option == '=' and params[0]:
        return 'DATE(' + field_name + ') = DATE(\'' + params[0] + '\')'
    if option == 'not_equal' and params[0]:
        return 'DATE(' + field_name + ') != DATE(\'' + params[0] + '\')'
    if option == 'greater_than' and params[0]:
        return 'DATE(' + field_name + ') > DATE(\'' + params[0] + '\')'
    if option == 'less_than' and params[0]:
        return 'DATE(' + field_name + ') < DATE(\'' + params[0] + '\')'
    if option == 'between' and params[0] and params[1]:
        return 'DATE(' + field_name + ') BETWEEN DATE(\'' + params[0] \
            + '\') AND DATE(\'' + params[1] + '\')'
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

def get_multienum_filter_in_mysql_format(field_name, values):
    if len(values) > 0:
        query = '('
        for option in values:
            if query != '(':
                query += " OR "
            query += field_name + " like '%^" + option + "^%'"
        query += ')'
        return query
    else:
        return None

def get_default_role():
    default_role = settings.DEFAULT_ROLE
    try:
        return Role.objects.get(name=default_role)
    except:
        role = Role(name=default_role)
        role.save()
        return role

def create_portal_user(contact):
    username = contact['email1']
    password = User.objects.make_random_password()
    try:
        user = User.objects.get(username = username)
        return JsonResponse({
            "status" : "Error",
            "error" : "An account with this email already exists"
        }, status = 400)
    except:
        pass
    user = User.objects.create_user(
        username = username,
        email = username,
        password = password,
        first_name = contact['first_name'],
        last_name = contact['last_name']
     )
    UserAttr(
        user = user,
        contact_id = contact['id'],
        account_id = contact['account_id']
    ).save()
    default_role = get_default_role()
    if default_role:
        RoleUser(
            user = user,
            role = default_role
        ).save()
    contact2 = Bean('Contacts')
    contact2['id'] = contact['id']
    contact2['joomla_account_id'] = user.id
    contact2['joomla_account_access'] = password
    SuiteCRM().save_bean(contact2)
    return JsonResponse({"success" : True})

def disable_portal_user(contact):
    try:
        user = User.objects.get(username = contact['email1'])
        user.is_active = False
        user.save()
        return JsonResponse({"success" : True})
    except:
        return JsonResponse({
            "status" : "Error",
            "error" : "Error dissabling account"
        }, status = 400)

def enable_portal_user(contact):
    try:
        user = User.objects.get(username = contact['email1'])
        user.is_active = True
        user.save()
        return JsonResponse({"success" : True})
    except:
        return JsonResponse({
            "status" : "Error",
            "error" : "Error enabling account"
        }, status = 400)

def user_can_read_record(user, module, id):
    try:
        if user_is_linked_to_record(user, module, id):
            return True
        module_def = ModuleDefinitionFactory.get_module_definition(module)
        if module_def.contacts_link_type == LinkType.NONE:
            return True
    except:
        pass
    return False

def user_is_linked_to_record(user, module, id):
    try:
        module_def = ModuleDefinitionFactory.get_module_definition(module)
        user_type = user.userattr.user_type
        if user_type == 'account':
            related_module = 'Accounts'
            related_id = user.userattr.account_id
            link_type = module_def.accounts_link_type
            link_name = module_def.accounts_link_name
        else:
            related_module = 'Contacts'
            related_id = user.userattr.contact_id
            link_type = module_def.contacts_link_type
            link_name = module_def.contacts_link_name

        if link_type == LinkType.RELATED:
            filter_query = module.lower() + '.id = \'' + id + '\' AND '
            filter_query += get_filter_related(
                module,
                link_name,
                related_id
            )
            records = SuiteCRM().get_bean_list(
                module,
                max_results = 1,
                query = filter_query
            )
        elif link_type == LinkType.RELATIONSHIP:
            records = SuiteCRM().get_relationships(
                related_module,
                related_id,
                link_name,
                related_fields = ['id'],
                limit = 1,
                related_module_query = module.lower() + '.id = \'' + id + '\''
            )
        elif module_def.contacts_link_type == LinkType.PARENT:
            filter_query = module.lower() + '.id = \'' + id + '\' AND '
            filter_query += get_filter_parent(
                module,
                related_module,
                related_id
            )
            records = SuiteCRM().get_bean_list(
                module,
                max_results = 1,
                query = filter_query
            )
        if records['entry_list'][0]['id'] == id:
            return True
    except:
        pass
    return False

def get_module_labels():
    module_labels = {}
    try:
        available_modules = get_available_modules()
        for key, module in available_modules.items():
            module_labels[key] = module['module_label']
    except:
        pass
    return module_labels

def get_available_modules():
    available_modules = OrderedDict()
    try:
        all_modules = SuiteCRMCached().get_available_modules()['modules']
        for module in all_modules:
            if module['module_key'] not in FORBIDDEN_MODULES:
                available_modules[module['module_key']] = module
    except Exception as e:
        pass
    return available_modules

def encode_multienum(values):
    if len(values) > 0:
        return '^' + '^,^'.join(values) + '^'
    else:
        return ''

def iso_to_datetime(value):
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M')\
            .strftime(settings.SUITECRM_DATETIME_FORMAT)
    except:
        return value

def get_module_view_fields(module, view):
    ordered_module_fields = []
    try:
        view_def = Layout.objects.get(module=module, view=view)
        fields = json.loads(view_def.fields)
        module_fields = SuiteCRMCached().get_module_fields(module)['module_fields']
        remove_colon_of_field_labels(module_fields)
        for row in fields:
            row_fields = []
            for field in row:
                if field in module_fields:
                    row_fields.append(module_fields[field])
                elif not field:
                    row_fields.append(None)
            ordered_module_fields.append(row_fields)
    except Exception:
        pass
    return ordered_module_fields

def get_bean_from_post(module, view, data):
    module_fields = SuiteCRMCached().get_module_fields(module)['module_fields']
    view_def = Layout.objects.get(module=module, view=view)
    fields = json.loads(view_def.fields)
    bean = Bean(module)
    for row in fields:
        for field in row:
            if field in module_fields:
                if field in data:
                    value = data[field]
                    field_def = module_fields[field]
                    field_type = field_def['type']
                    if field_type == 'multienum':
                        bean[field] = encode_multienum(
                            data.getlist(field)
                        )
                    elif field_type == 'datetime' or field_type == 'datetimecombo':
                        bean[field] = iso_to_datetime(value)
                    elif field_type == 'relate':
                        relate_id_field = field_def['id_name']
                        if relate_id_field in data:
                            bean[relate_id_field] = data[relate_id_field]
                    elif field_type == 'parent_type':
                        if 'parent_id' in data:
                            bean[field] = value
                            bean['parent_id'] = data['parent_id']
                    else:
                        bean[field] = value
    return bean

def relate_bean_with_user(bean, user):
    result = {
        'contact_related' : False,
        'account_related' : False
    }
    try:
        result['contact_related'] = relate_bean_with_contact(
            bean,
            user.userattr.contact_id
        )
    except Exception:
        pass
    try:
        result['account_related'] = relate_bean_with_account(
            bean,
            user.userattr.account_id
        )
    except Exception:
        pass
    return result

def relate_bean_with_contact(bean, contact_id):
    try:
        module = bean.module
        if not contact_id or not module:
            return False
        module_def = ModuleDefinitionFactory.get_module_definition(module)
        if module_def.contacts_link_type == LinkType.RELATED:
            bean[module_def.contacts_link_name] = contact_id
            SuiteCRM().save_bean(bean)
        elif module_def.contacts_link_type == LinkType.RELATIONSHIP:
            result = SuiteCRM().set_relationship(
                'Contacts',
                contact_id,
                module_def.contacts_link_name,
                related_ids = [bean['id']]
            )
            if result['created'] != 1:
                return False
        elif module_def.contacts_link_type == LinkType.PARENT:
            bean['parent_type'] = 'Contacts'
            bean['parent_id'] = contact_id
            SuiteCRM().save_bean(bean)
    except:
        return False
    return True

def relate_bean_with_account(bean, account_id):
    try:
        module = bean.module
        if not account_id or not module:
            return False
        module_def = ModuleDefinitionFactory.get_module_definition(module)
        if module_def.accounts_link_type == LinkType.RELATED:
            bean[module_def.accounts_link_name] = account_id
            SuiteCRM().save_bean(bean)
        elif module_def.accounts_link_type == LinkType.RELATIONSHIP:
            result = SuiteCRM().set_relationship(
                'Accounts',
                account_id,
                module_def.accounts_link_name,
                related_ids = [bean['id']]
            )
            if result['created'] != 1:
                return False
        elif module_def.accounts_link_type == LinkType.PARENT:
            bean['parent_type'] = 'Accounts'
            bean['parent_id'] = account_id
            SuiteCRM().save_bean(bean)
    except:
        return False
    return True
