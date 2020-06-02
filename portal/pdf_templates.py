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
from .models import PortalSetting

AOS_PDF_TEMPLATES_FIELDS = [
    'id',
    'name',
    'description'
]


def get_aos_invoices_pdf_templates():
    return SuiteCRM().get_bean_list(
        'AOS_PDF_Templates',
        "aos_pdf_templates.type = 'AOS_Invoices'",
        select_fields=AOS_PDF_TEMPLATES_FIELDS
    )


def get_aos_quotes_pdf_templates():
    return SuiteCRM().get_bean_list(
        'AOS_PDF_Templates',
        "aos_pdf_templates.type = 'AOS_Quotes'",
        select_fields=AOS_PDF_TEMPLATES_FIELDS
    )


def get_aos_contracts_pdf_templates():
    return SuiteCRM().get_bean_list(
        'AOS_PDF_Templates',
        "aos_pdf_templates.type = 'AOS_Contracts'",
        select_fields=AOS_PDF_TEMPLATES_FIELDS
    )


def get_pdf_template_id(module):
    try:
        t = PortalSetting.objects.get(name='pdf_template_id_' + module.lower())
        return t.value
    except Exception:
        return None


def set_pdf_template_id(module, template_id):
    try:
        t = PortalSetting.objects.get(name='pdf_template_id_' + module.lower())
        t.value = template_id
        t.save()
    except Exception:
        PortalSetting(
            name='pdf_template_id_' + module.lower(),
            value=template_id
        ).save()
