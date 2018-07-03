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

AOS_PRODUCTS_QUOTES_FIELDS = [
    'name',
    'item_description',
    'product_id',
    'product_qty',
    'product_list_price',
    'discount',
    'product_discount',
    'product_unit_price',
    'vat',
    'vat_amt',
    'product_total_price'
]

def get_aos_quotes_record(module, id):
    return SuiteCRM().get_bean(
        module,
        id,
        link_name_to_fields_array = [
            {
                'name' : 'aos_products_quotes',
                'value' : AOS_PRODUCTS_QUOTES_FIELDS
            }
        ]
    )
