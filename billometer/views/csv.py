
import logging
from django.http import HttpResponse
from django.views import generic

LOG = logging.getLogger(__name__)


class CSVExportView(generic.View):

    """
    A base view for get overview in CSV format
    """

    def get(self, request, *args, **kwargs):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="summary.csv"'

        raise NotImplementedError
