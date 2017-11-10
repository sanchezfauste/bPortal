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

def remove_colon_of_field_labels(module_fields):
    for field in module_fields:
        label = module_fields[field]['label']
        if len(label) > 0 and label[-1] == ':':
            module_fields[field]['label'] = label[:-1]

def get_user_accesible_modules(user):
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

def user_can_read_module(user, module):
    return _user_can_perform_action_on_module(user, "read", module)

def user_can_create_module(user, module):
    return _user_can_perform_action_on_module(user, "create", module)

def user_can_edit_module(user, module):
    return _user_can_perform_action_on_module(user, "edit", module)

def user_can_delete_module(user, module):
    return _user_can_perform_action_on_module(user, "delete", module)

def _user_can_perform_action_on_module(user, action, module):
    return RolePermission.objects.filter(
        role=user.roleuser.role,
        module=module,
        grant=True,
        action=action
    ).exists()
