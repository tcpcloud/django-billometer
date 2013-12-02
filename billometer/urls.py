
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers

from .views import *

router_api_v1 = routers.SimpleRouter()


urlpatterns = patterns('billometer.views',
    url(r'^auth/', include('openstack_auth.urls')),
    url(r'^api/v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^v1/', include(router_api_v1.urls)),
    url(r'^v1/project-list/(?P<user_id>[^/]+)/(?P<start_date>[\w\-\_\.]+)/(?P<end_date>[\w\-\_\.]+)/$', 'project_list', name='project_list'),
    url(r'^v1/project-list/(?P<user_id>[^/]+)/$', 'project_list', name='project_list'),
    url(r'^v1/quota-list/(?P<user_id>[^/]+)/$', QuotaListView.as_view(), name='quota_list'),
    url(r'^v1/project-info/(?P<project_id>[^/]+)/$', 'project_info', name='project_info'),
    url(r'^v1/project-summary/(?P<project_id>[^/]+)/(?P<start>[\w\-\_\.]+)/(?P<end>[\w\-\_\.]+)/$', 'project_summary', name='project_summary'),
    url(r'^v1/project-summary/(?P<project_id>[^/]+)/$', 'project_summary', name='project_summary'),
    url(r'^v1/project-update/(?P<project_id>[^/]+)/$', 'project_update', name='project_update'),
    url(r'^v1/resource-list/(?P<project_id>[^/]+)/$', 'resource_list', name='resource_list'),
    url(r'^v1/quota-sync/(?P<project_id>[^/]+)/$', QuotaSyncView.as_view(), name='quota_sync'),
    url(r'^v1/server-list/(?P<project_id>[^/]+)/(?P<start_date>[\w\-\_\.]+)/(?P<end_date>[\w\-\_\.]+)/$', InstanceResourceView.as_view(), name='server_list'),
    url(r'^v1/server-list/(?P<project_id>[^/]+)/$', InstanceResourceView.as_view(), name='server_list'),
    url(r'^v1/volume-list/(?P<project_id>[^/]+)/(?P<start_date>[\w\-\_\.]+)/(?P<end_date>[\w\-\_\.]+)/$', VolumeResourceView.as_view(), name='volume_list'),
    url(r'^v1/volume-list/(?P<project_id>[^/]+)/$', VolumeResourceView.as_view(), name='volume_list'),
    url(r'^v1/address-list/(?P<project_id>[^/]+)/(?P<start_date>[\w\-\_\.]+)/(?P<end_date>[\w\-\_\.]+)/$', AddressResourceView.as_view(), name='address_list'),
    url(r'^v1/address-list/(?P<project_id>[^/]+)/$', AddressResourceView.as_view(), name='address_list'),
    url(r'^v1/network-list/(?P<project_id>[^/]+)/(?P<start_date>[\w\-\_\.]+)/(?P<end_date>[\w\-\_\.]+)/$', NetworkResourceView.as_view(), name='network_list'),
    url(r'^v1/network-list/(?P<project_id>[^/]+)/$', NetworkResourceView.as_view(), name='network_list'),
    url(r'^v1/image-list/(?P<project_id>[^/]+)/(?P<start_date>[\w\-\_\.]+)/(?P<end_date>[\w\-\_\.]+)/$', ImageResourceView.as_view(), name='image_list'),
    url(r'^v1/image-list/(?P<project_id>[^/]+)/$', ImageResourceView.as_view(), name='image_list'),
    url(r'^v1/export-csv/(?P<project_id>[^/]+)/$', CSVExportView.as_view(), name='export_csv'),
    url(r'^v1/export-csv/(?P<project_id>[^/]+)/(?P<start>[\w\-\_\.]+)/(?P<end>[\w\-\_\.]+)/$', CSVExportView.as_view(), name='export_csv'),
    url(r'^v1/admin/rate-list/$', 'rate_list', name='admin_rate_list'),
    url(r'^v1/admin/quota-list/$', 'quota_list', name='admin_quota_list'),
) + staticfiles_urlpatterns()
