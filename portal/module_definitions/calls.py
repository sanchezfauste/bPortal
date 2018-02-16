#######################################################################
# Suite PY is a simple Python client for SuiteCRM API.

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

from module_definition import ModuleDefinition
from link_type import LinkType

class Calls(ModuleDefinition):

    @property
    def name(self):
        return 'Calls'

    @property
    def contacts_link_type(self):
        return LinkType.RELATIONSHIP

    @property
    def contacts_link_name(self):
        return 'calls'

    @property
    def accounts_link_type(self):
        return LinkType.PARENT

    @property
    def accounts_link_name(self):
        return 'parent_id'
