from __future__ import absolute_import, unicode_literals

import datetime
import functools
import logging
from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import available_attrs  # noqa
from django.utils.translation import ugettext_lazy as _
from rest_framework.renderers import JSONRenderer

LOG = logging.getLogger(__name__)


def now_iso():
    return datetime.date.today().isoformat()


class JSONResponse(HttpResponse):

    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(
            data, renderer_context={'indent': 2, 'ensure_asci': False})
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def handle_exception(view_func):
    """Performs handling and serializing exception.
    """

    @functools.wraps(view_func, assigned=available_attrs(view_func))
    def dec(request, *args, **kwargs):

        try:
            response = view_func(request, *args, **kwargs)

        except Exception as e:
            if settings.DEBUG:
                raise e
            response = JSONResponse({'error': 'Unexpected Error. '
                                     'Please contact Administrator.'})
            response.status_code = 500

        return response

    return dec
