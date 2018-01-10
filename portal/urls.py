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

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^modules/$', views.modules, name='modules'),
    url(r'^module/(?P<module>\w+)/list$', views.module_list, name='module_list'),
    url(r'^layouts/$', views.edit_layouts, name='edit_layouts'),
    url(r'^layout/list/(?P<module>\w+)/$', views.edit_list_layout, name='edit_list_layout'),
    url(r'^role/(?P<role>\w+)$', views.edit_role, name='edit_role'),
]
