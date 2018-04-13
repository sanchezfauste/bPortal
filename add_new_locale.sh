#!/bin/bash

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

echo -e -n "#############################################\n"
echo -e -n "#        bPortal - A SuiteCRM portal        #\n"
echo -e -n "#                                           #\n"
echo -e -n "#   Copyright (C) 2017-2018 BTACTIC, SCCL   #\n"
echo -e -n "#   Copyright (C) 2017-2018 Marc Sanchez    #\n"
echo -e -n "#############################################\n\n"

if [[ $# -ne 1 ]] ; then
    echo -e "Usage: $0 <locale_name>\n"
    echo -e "  <locale_name>    A locale name, either a language specification"
    echo -e "                   of the form ll or a combined language and country"
    echo -e "                   specification of the form ll_CC.\n"
    echo -e "                   Examples: it, de_AT, es, pt_BR. The language part"
    echo -e "                   is always in lower case and the country part in"
    echo -e "                   upper case. The separator is an underscore."
    exit 1
fi

ABSPATH=$(readlink -f $0)
ABSDIR=$(dirname $ABSPATH)

echo -e -n "Processing portal app locale messages...\n"
cd $ABSDIR/portal
django-admin makemessages -l $1

echo -e -n "\nProcessing bPortal project locale messages...\n"
cd $ABSDIR/bPortal
django-admin makemessages -l $1
