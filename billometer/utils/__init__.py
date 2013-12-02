
from billometer.utils.keystone import _get_client as keystone_client

"""
must be here because in keystone.py makes circural dependency
"""


def get_service_from_catalog(catalog, service_type):
    if catalog:
        for service in catalog:
            if service.type == service_type and service.enabled:
                return service
    return None


def get_service_catalog(client=None):
    service_catalog = []
    if not client:
        client = keystone_client()
        """
        auth_ref = getattr(client, "auth_ref", {})
        """
    else:
        """
        auth_ref = getattr(client, "auth_ref", {})
        """
        pass
    # TODO(majklk): v2 has serviceCatalog and v3 has only "catalog"
    """
    service_catalog = auth_ref.get("serviceCatalog", [])
    """
    return client.services.list()


def is_service_enabled(service, client=None):
    """expect service name like a compute, neutron, volume etc
    """

    service_catalog = get_service_catalog(client)
    service = get_service_from_catalog(service_catalog, service)

    if service:
        return True

    return False
