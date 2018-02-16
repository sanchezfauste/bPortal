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

from abc import ABCMeta
from accounts import Accounts
from tasks import Tasks
from calls import Calls
from meetings import Meetings
from emails import Emails
from documents import Documents
from opportunities import Opportunities
from leads import Leads
from campaigns import Campaigns
from cases import Cases
from bugs import Bugs
from contacts import Contacts
from aos_quotes import AOS_Quotes
from aos_invoices import AOS_Invoices
from aos_contracts import AOS_Contracts
from fp_events import FP_events
from project import Project
from module_definition_not_found_exception import ModuleDefinitionNotFoundException

class ModuleDefinitionFactory:

    __metaclass__ = ABCMeta

    @staticmethod
    def get_module_definition(module_name):
        if module_name == 'Accounts': return Accounts()
        if module_name == 'Tasks': return Tasks()
        if module_name == 'Calls': return Calls()
        if module_name == 'Meetings': return Meetings()
        if module_name == 'Emails': return Emails()
        if module_name == 'Documents': return Documents()
        if module_name == 'Opportunities': return Opportunities()
        if module_name == 'Leads': return Leads()
        if module_name == 'Campaigns': return Campaigns()
        if module_name == 'Cases': return Cases()
        if module_name == 'Bugs': return Bugs()
        if module_name == 'Contacts': return Contacts()
        if module_name == 'AOS_Quotes': return AOS_Quotes()
        if module_name == 'AOS_Invoices': return AOS_Invoices()
        if module_name == 'AOS_Contracts': return AOS_Contracts()
        if module_name == 'FP_events': return FP_events()
        if module_name == 'Project': return Project()
        raise ModuleDefinitionNotFoundException(module_name)
