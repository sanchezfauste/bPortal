/**************************************************************************
 * bPortal is a SuiteCRM portal written using django project.
 * Copyright (C) 2017 Marc Sanchez Fauste
 * Copyright (C) 2017 BTACTIC, SCCL

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

function save_role_permissions() {

    var permissions = $('#module_permissions tr td input').map(function() {
        return [[
            $(this).attr('module'),
            $(this).attr('permission'),
            $(this).is(':checked')
        ]];
    }).get();

    var data = {"permissions" : permissions};

    $.ajax({
        type: "POST",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        error: function(response) {
            alert(response.responseJSON.error);
        },
        success: function(response) {
            alert(response.msg);
        }
    });

}
