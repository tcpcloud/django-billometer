
import logging
from billometer.models import Project
from billometer.utils import cinder
from billometer.utils.keystone import projects_for_user
from django.views import generic

from .resources import BaseResourceView
from .utils import JSONResponse

LOG = logging.getLogger(__name__)


class QuotaListView(BaseResourceView):

    """
    quotas view
    """

    def get(self, request, *args, **kwargs):

        project_names = []

        projects = projects_for_user(self.kwargs.get("user_id"))

        for project in projects:
            project_names.append(project['name'])

        project_list = []

        projects = Project.objects.filter(name__in=project_names)

        for project in projects:

            project_list.append(project.get_quotas_list())

        return JSONResponse(project_list)


def quota_list(request):

    project_list = []
    projects = Project.objects.all()

    for project in projects:

        project_list.append(project.get_quotas_list())

    return JSONResponse(project_list)


def rate_list(request):

    project_list = []
    projects = Project.objects.all()

    for project in projects:

        glance_image = volume_easy = volume_7k = volume_10k = volume_15k = "-"

        memory_price = cpu_price = neutron_ip = '-'

        for resource_type in project.resourcetype_set.all():
            if resource_type.resource == "nova.memory":
                memory_price = resource_type.default_price
            if resource_type.resource == "nova.cpu":
                cpu_price = resource_type.default_price
            if resource_type.resource == "neutron.floating_ip":
                neutron_ip = resource_type.default_price
            if resource_type.resource == "glance.image":
                glance_image = resource_type.default_price
            if resource_type.name == "EasyTier":
                volume_easy = resource_type.default_price
            if resource_type.name == "7k2_SAS":
                volume_7k = resource_type.default_price
            if resource_type.name == "10k_SAS":
                volume_10k = resource_type.default_price
            if resource_type.name == "15k_SAS":
                volume_15k = resource_type.default_price

        project_list.append({
            'name': project.name,
            'uuid': project.openstack_tenant,
            'memory': memory_price,
            'cpu': cpu_price,
            'neutron_ip': neutron_ip,
            'glance_image': glance_image,
            'disk_EasyTier': volume_easy,
            'disk_7k2': volume_7k,
            'disk_10k': volume_10k,
            'disk_15k': volume_15k,
        })

    return JSONResponse(project_list)


class QuotaSyncView(generic.View):

    """
    A base view for get overview in CSV format
    """

    def get(self, request, *args, **kwargs):

        project = Project.objects.get(openstack_tenant=self.kwargs['project_id'])

        extra = project.extra.copy()
        extra.update(cinder.get_quotas(project.name, project.openstack_tenant))
        extra.update(cinder.get_quotas(project.name, project.openstack_tenant))
        project.extra = extra
        project.save()

        return JSONResponse(project.extra)
