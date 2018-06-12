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

from abc import ABCMeta, abstractproperty
from django.conf import settings

class ModuleDefinition:

    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def contacts_link_type(self):
        pass

    @abstractproperty
    def contacts_link_name(self):
        pass

    @abstractproperty
    def accounts_link_type(self):
        pass

    @abstractproperty
    def accounts_link_name(self):
        pass

    @property
    def custom_where(self):
        return None

    @property
    def custom_dropdown_where(self):
        return None

    @property
    def default_values(self):
        return {}

    @property
    def default_order_by_field(self):
        return settings.DEFAULT_ORDER_BY_FIELD

    @property
    def default_order(self):
        return settings.DEFAULT_ORDER

    @staticmethod
    def before_save_on_create_hook(bean, request):
        pass

    @staticmethod
    def before_save_on_edit_hook(bean, request):
        pass
