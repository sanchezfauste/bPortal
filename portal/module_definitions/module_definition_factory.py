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

from abc import ABCMeta
from .module_definition_not_found_exception import ModuleDefinitionNotFoundException
from importlib import import_module


class ModuleDefinitionFactory:

    __metaclass__ = ABCMeta

    @staticmethod
    def get_module_definition(module_name):
        try:
            mod_def = import_module(
                'portal.module_definitions.custom.' + module_name.lower()
            )
            md = getattr(mod_def, module_name)
            return md()
        except Exception:
            pass
        try:
            mod_def = import_module(
                'portal.module_definitions.' + module_name.lower()
            )
            md = getattr(mod_def, module_name)
            return md()
        except Exception:
            pass
        raise ModuleDefinitionNotFoundException(module_name)
