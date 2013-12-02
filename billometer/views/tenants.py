import logging
from datetime import date

import simplejson
import six
from billometer.conf import EXTRA_RESOURCES
from billometer.models import Project
from billometer.utils import cinder
from django.views.decorators.csrf import csrf_exempt

from ..serializers import ProjectSerializer
from .resources import get_data
from .utils import JSONResponse

LOG = logging.getLogger(__name__)


def project_list(request, user_id, start_date=None, end_date=None):
    return JSONResponse(get_data(user_id, start_date, end_date))


@csrf_exempt
def project_update(request, project_id):

    project = Project.objects.get(openstack_tenant=project_id)
    project_data = {}
    if project:

        if request.method == "GET":
            project_data = ProjectSerializer(project).data

        if request.method == "POST":
            data = simplejson.loads(request.body)
            # allow only update existing
            serializer = ProjectSerializer(project, data=data)

            if not serializer.is_valid():
                return JSONResponse(
                    {"errors": "Project is not valid !"})
            else:
                serializer.save()

                # update

                data = {
                    "cores": int(project.extra.get("cpu")),
                    "ram": int(project.extra.get("memory")),
                }

                try:
                    extra_data = {}
                    for key, val in six.iteritems(EXTRA_RESOURCES):
                        if key in data:
                            extra_data[key] = int(project.extra.get(key))
                    cinder.set_quotas(project.name, project.openstack_tenant, extra_data)
                except Exception, e:
                    LOG.error(str(e))

                project_data = ProjectSerializer(serializer.object).data

    else:
        return JSONResponse("missing project_id param")

    return JSONResponse(project_data)


@csrf_exempt
def project_info(request, project_id):

    project_data = Project.objects.filter(openstack_tenant=project_id).values()

    return JSONResponse(project_data[0])


@csrf_exempt
def project_summary(request, project_id, start=None, end=None):

    project = Project.objects.get(openstack_tenant=project_id)
    project_data = {}

    if start is None:
        start = date.today()
    if end is None:
        end = date.today()

    if project:
        project_data = project.get_overview(start, end)
    else:
        return JSONResponse("missing project_id param")

    return JSONResponse(project_data)
