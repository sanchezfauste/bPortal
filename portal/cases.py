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

from suitepy.suitecrm import SuiteCRM

NOTE_FIELDS = [
    'id',
    'name',
    'date_entered',
    'date_modified',
    'description',
    'filename',
    'file_url'
]

CASE_UPDATE_FIELDS = [
    'id',
    'name',
    'date_entered',
    'date_modified',
    'description',
    'contact',
    'contact_id',
    'internal',
    'assigned_user_id'
]

CONTACT_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'date_entered',
    'date_modified',
    'description',
    'portal_user_type',
    'account_id'
]

USER_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'date_entered',
    'date_modified',
    'description'
]

def get_case(case_id):
    return SuiteCRM().get_bean(
        'Cases',
        case_id,
        link_name_to_fields_array = [
            {
                'name' : 'notes',
                'value' : NOTE_FIELDS
            },
            {
                'name' : 'contacts',
                'value' : CONTACT_FIELDS
            }
        ]
    )

def get_case_updates(case_id):
    return SuiteCRM().get_relationships(
        'Cases',
        case_id,
        'aop_case_updates',
        related_fields = CASE_UPDATE_FIELDS,
        related_module_link_name_to_fields_array = [
            {
                'name' : 'notes',
                'value' : NOTE_FIELDS
            },
            {
                'name' : 'assigned_user_link',
                'value' : USER_FIELDS
            },
            {
                'name' : 'contact',
                'value' : CONTACT_FIELDS
            }
        ],
        order_by = 'date_entered',
        related_module_query = 'aop_case_updates.internal = 0'
    )
