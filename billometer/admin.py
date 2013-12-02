
from django.contrib import admin
from django.utils.html import mark_safe

from billometer.models import Project, \
    ResourceType, ResourceInstance, ResourceInstanceData


class ResourceInstanceDataInline(admin.TabularInline):
    model = ResourceInstanceData
    extra = 1
    suit_classes = 'suit-tab suit-tab-resource-instance-data'


class ResourceInstanceInline(admin.TabularInline):
    model = ResourceInstance
    extra = 1
    suit_classes = 'suit-tab suit-tab-resource-instance'


class ResourceTypeInline(admin.TabularInline):
    model = ResourceType
    extra = 1
    suit_classes = 'suit-tab suit-tab-resource-type'


class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        'name', 'openstack_tenant', 'customer_name', 'customer_id', 'extra', 'get_links')
    inlines = [ResourceTypeInline]

    def get_links(self, instance):
        links = []
        links.append('<a href="/v1/server-list/%s/">Server API</a>' %
                     instance.openstack_tenant)
        links.append('<a href="/v1/quota-sync/%s/">Sync Quotas</a>' %
                     instance.openstack_tenant)
        return mark_safe(' | '.join(links))
    get_links.short_description = u"Actions"

admin.site.register(Project, ProjectAdmin)


class ResourceInstanceDataAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'resource', 'date', 'closed', 'value', 'price')
    list_filter = ('resource', 'date')

admin.site.register(ResourceInstanceData, ResourceInstanceDataAdmin)


class ResourceInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'openstack_id', 'resource_type', 'is_active', 'extra')
    list_filter = ('resource_type',)

    inlines = [ResourceInstanceDataInline, ]

admin.site.register(ResourceInstance, ResourceInstanceAdmin)


class ResourceTypeAdmin(admin.ModelAdmin):

    list_display = ('name', 'openstack_id', 'resource', 'project',
                    'default_price', 'default_threshold', 'extra')
    list_filter = ('resource', 'project',)

    inlines = [ResourceInstanceInline]

admin.site.register(ResourceType, ResourceTypeAdmin)
