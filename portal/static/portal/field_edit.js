/**************************************************************************
 * bPortal is a SuiteCRM portal written using django project.
 * Copyright (C) 2017-2018 BTACTIC, SCCL
 * Copyright (C) 2017-2018 Marc Sanchez Fauste

 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.

 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *************************************************************************/

function update_dynamicenum(field, subfield) {
    if (document.getElementById(subfield) != null) {
        var de_key = document.getElementById(field).value;
        var selector = document.getElementById(subfield);

        var current = [];
        for (var i = 0; i < selector.length; i++) {
            if (selector.options[i].selected) current.push(selector.options[i].value);
        }

        document.getElementById(subfield).innerHTML = '';

        for (var key in de_entries[subfield]) {
            if (key.indexOf(de_key + '_') == 0 || key == '') {
                selector.options[selector.options.length] = new Option(de_entries[subfield][key], key);
            }
        }

        for (var item in current) {
            for (var k = 0; k < selector.length; k++) {
                if (selector.options[k].value == current[item]) {
                    selector[k].selected = true;
                }
            }
        }
    }
}
