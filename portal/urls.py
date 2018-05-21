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

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^modules/$', views.modules, name='modules'),
    url(r'^module/(?P<module>\w+)/list$', views.module_list, name='module_list'),
    url(r'^module/(?P<module>\w+)/detail/(?P<id>[\w-]+)/$', views.module_detail, name='module_detail'),
    url(r'^module/(?P<module>\w+)/edit/(?P<id>[\w-]+)/$', views.module_edit, name='module_edit'),
    url(r'^module/(?P<module>\w+)/create/$', views.module_create, name='module_create'),
    url(r'^module/(?P<module>\w+)/remove/$', views.module_remove_record, name='module_remove_record'),
    url(r'^layouts/$', views.edit_layouts, name='edit_layouts'),
    url(r'^user_records/(?P<module>\w+)/$', views.user_records, name='user_records'),
    url(r'^layout/list/(?P<module>\w+)/$', views.edit_list_layout, name='edit_list_layout'),
    url(r'^layout/filter/(?P<module>\w+)/$', views.edit_filter_layout, name='edit_filter_layout'),
    url(r'^layout/detail/(?P<module>\w+)/$', views.edit_detail_layout, name='edit_detail_layout'),
    url(r'^layout/edit/(?P<module>\w+)/$', views.edit_edit_layout, name='edit_edit_layout'),
    url(r'^layout/create/(?P<module>\w+)/$', views.edit_create_layout, name='edit_create_layout'),
    url(r'^roles/$', views.edit_roles, name='edit_roles'),
    url(r'^role/(?P<role>\w+)$', views.edit_role, name='edit_role'),
    url(r'^roles/delete$', views.delete_role, name='delete_role'),
    url(r'^roles/create$', views.create_role, name='create_role'),
    url(r'^note_attachment/(?P<id>[\w-]+)/$', views.note_attachment, name='note_attachment'),
    url(r'^add_case_update/$', views.add_case_update, name='add_case_update'),
    url(r'^close_case/$', views.close_case, name='close_case'),
    url(r'^reopen_case/$', views.reopen_case, name='reopen_case'),
    url(r'^users/$', views.edit_users, name='edit_users'),
    url(r'^user/(?P<user_id>\d+)$', views.edit_user, name='edit_user'),
    url(r'^user_profile/$', views.user_profile, name='user_profile'),
    url(r'^index.php$', views.crm_entry_point, name='crm_entry_point'),
]
