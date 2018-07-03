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

from django import template
import HTMLParser
from datetime import datetime
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.staticfiles import finders

register = template.Library()

@register.filter(name='get')
def get(dict, key):
    try:
        return dict[key]
    except:
        return ''

@register.filter(name='getlist')
def getlist(dict, key):
    try:
        return dict.getlist(key)
    except:
        return ''

@register.filter(name='get_list_str')
def get_list_str(values):
    str = '['
    for i in xrange(len(values)):
        str += "'" + values[i] + "'"
        if i < len(values) - 1:
            str += ","
    str += ']'
    return str

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

@register.filter(name='get_module_dark_svg')
def get_module_dark_svg(module):
    custom_module_img = 'portal/img/custom/modules/dark/' + module + '.svg'
    module_img = 'portal/img/modules/dark/' + module + '.svg'
    default_img = 'portal/img/modules/dark/basic.svg'
    if finders.find(custom_module_img):
        return custom_module_img
    elif finders.find(module_img):
        return module_img
    else:
        return default_img

@register.filter(name='get_module_light_svg')
def get_module_light_svg(module):
    custom_module_img = 'portal/img/custom/modules/light/' + module + '.svg'
    module_img = 'portal/img/modules/light/' + module + '.svg'
    default_img = 'portal/img/modules/light/basic.svg'
    if finders.find(custom_module_img):
        return custom_module_img
    elif finders.find(module_img):
        return module_img
    else:
        return default_img

@register.filter(name='get_module_ico')
def get_module_ico(module):
    custom_module_img = 'portal/img/custom/modules/favicon/' + module + '.ico'
    module_img = 'portal/img/modules/favicon/' + module + '.ico'
    default_img = 'portal/img/modules/favicon/basic.ico'
    if finders.find(custom_module_img):
        return custom_module_img
    elif finders.find(module_img):
        return module_img
    else:
        return default_img

@register.filter(name='add')
def add(a, b):
    try:
        return float(a) + float(b)
    except Exception:
        return 0
