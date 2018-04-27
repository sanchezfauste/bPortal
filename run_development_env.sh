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


ABSPATH=$(readlink -f $0)
ABSDIR=$(dirname $ABSPATH)

ENV_DIR=env
ENV_PATH=$ABSDIR/$ENV_DIR

if [ ! -f $ENV_PATH/bin/activate ]; then
    echo -e "[ERROR] Unable to find python virtualenv. Exiting."
    exit 1
fi

source $ENV_PATH/bin/activate
python $ABSDIR/manage.py runserver 0.0.0.0:8080

deactivate
