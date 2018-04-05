#######################################################################
# bPortal is a SuiteCRM portal written using django project.

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

from django import template
import HTMLParser
from datetime import datetime
from django.conf import settings
from django.utils.translation import gettext as _

register = template.Library()

@register.filter(name='get')
def get(dict, key):
    try:
        return dict[key]
    except:
        return ''

@register.filter(name='get_label')
def get_label(dict, key):
    try:
        return dict[key]
    except:
        return key

@register.filter(name='decode')
def decode(value):
    return HTMLParser.HTMLParser().unescape(value)

@register.filter(name='format_date')
def format_date(value):
    try:
        # Translators: Format for date fields following python date format.
        return datetime.strptime(value, settings.SUITECRM_DATE_FORMAT)\
            .strftime(_('%d/%m/%Y'))
    except:
        return value

@register.filter(name='format_time')
def format_time(value):
    try:
        # Translators: Format for time fields following python date format.
        return datetime.strptime(value, settings.SUITECRM_TIME_FORMAT)\
            .strftime(_('%H:%M'))
    except:
        return value

@register.filter(name='format_datetime')
def format_datetime(value):
    try:
        # Translators: Format for datetime fields following python date format.
        return datetime.strptime(value, settings.SUITECRM_DATETIME_FORMAT)\
            .strftime(_('%d/%m/%Y %H:%M'))
    except:
        return value

@register.filter(name='iso_datetime')
def iso_datetime(value):
    try:
        return datetime.strptime(value, settings.SUITECRM_DATETIME_FORMAT)\
            .strftime('%Y-%m-%dT%H:%M')
    except:
        return value

@register.filter(name='unencode_multienum')
def unencode_multienum(value):
    if len(value) >= 2 and value[0] == '^' and value[-1] == '^':
        value = value[1:-1]
    return value.split('^,^')
