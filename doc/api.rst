
======================
Billometer REST API v1
======================

GET /v1/project-list/<user_id>/<start_date>/<end_date>/
-------------------------------------------------------

.. code-block:: bash

    majklk@samsung:~⟫ http http://10.10.10.100:9753/v1/project-list/4f241af262644040960d9542f61eda00/2015-10-01/2015-10-04/
    HTTP/1.0 200 OK
    Content-Type: application/json
    Date: Sun, 04 Oct 2015 20:40:59 GMT
    Server: WSGIServer/0.1 Python/2.7.6

    [
        {
            "address_count": 2, 
            "address_price": 0.003334, 
            "image_count": 0, 
            "image_price": 0, 
            "instance_count": 4, 
            "instance_price": 37.599849, 
            "name": "tcp_lab_tux", 
            "uuid": "28604557ea9b46028fbc33b899d85a99", 
            "volume_count": 7, 
            "volume_price": 2.737734
        }, 
    ]

GET /v1/project-summary/<tenant_id>/<start_date>/<end_date>/
------------------------------------------------------------

.. code-block:: bash

    majklk@samsung:~⟫ http http://10.10.10.100:9753/v1/project-summary/4a69b129bee3446b8e8b72d664777dc8/2015-8-1/2015-10-20/
    HTTP/1.0 200 OK
    Content-Type: application/json
    Date: Mon, 05 Oct 2015 12:55:20 GMT
    Server: WSGIServer/0.1 Python/2.7.6

    [
        {
            "name": "VCPU", 
            "price": 0.0, 
            "rate": 0.821904, 
            "value": 0
        }, 
        {
            "name": "RAM", 
            "price": 0.0, 
            "rate": 0.000369, 
            "value": 0
        }, 
        {
            "name": "Images", 
            "price": 0.0, 
            "rate": 0.002739, 
        }, 
        {
            "name": "Easy tier", 
            "price": 0.0, 
            "rate": 0.041082, 
            "value": 0
        }, 
        {
            "name": "Network rx", 
            "price": 0.0, 
            "rate": 0.0, 
            "value": 5525974640.0
        }, 
        {
            "name": "10k2 sas", 
            "price": 0.0, 
            "rate": 0.027383, 
            "value": 0
        }, 
        {
            "name": "15k2 sas", 
            "price": 0.0, 
            "rate": 0.034232, 
            "value": 0
        }, 
        {
            "name": "Network tx", 
            "price": 0.0, 
            "rate": 0.0, 
            "value": 5767403090.0
        }, 
        {
            "name": "7k2 sas", 
            "price": 9.8880096, 
            "rate": 0.008205, 
            "value": 1205.12
        }, 
        {
            "name": "Resource Allocation", 
            "price": 2579.15424, 
            "rate": null, 
            "value": null
        }, 
        {
            "name": "Price Total", 
            "price": 2579.15424, 
            "rate": null, 
            "value": null
        }
    ]


.. note::

    date value format ``YYYY-MM-DD``


GET /v1/resource-list/<tenant_id>/<start_date>/<end_date>/
----------------------------------------------------------

List of project resources with their thresholds and rates.

.. code-block:: bash

    majklk@samsung:~⟫ http http://10.10.10.100:9753/v1/project-summary/b1fe992b79904336a79a441dd6350569/
    HTTP/1.0 200 OK
    Content-Type: application/json
    Date: Thu, 01 Oct 2015 13:36:28 GMT
    Server: WSGIServer/0.1 Python/2.7.6

    [
        {
            "name": "VCPU", 
            "price": 0.0, 
            "rate": 0.821904, 
            "value": 0
        }, 
        {
            "name": "RAM", 
            "price": 0.0, 
            "rate": 0.000369, 
            "value": 0
        }, 
        {
            "default_price": 1.0, 
            "default_threshold": 0.0, 
            "id": 872, 
            "name": "ip", 
            "resource": "neutron.floating_ip"
        }, 
        {
            "default_price": 0.034232, 
            "default_threshold": 0.0, 
            "id": 918, 
            "name": "15k_SAS", 
            "resource": "cinder.volume"
        }, 
        {
            "default_price": 0.041082, 
            "default_threshold": 0.0, 
            "id": 919, 
            "name": "EasyTier", 
            "resource": "cinder.volume"
        }, 
        {
            "default_price": 0.008205, 
            "default_threshold": 0.0, 
            "id": 920, 
            "name": "7k2_SAS", 
            "resource": "cinder.volume"
        }, 
        {
            "default_price": 0.027383, 
            "default_threshold": 0.0, 
            "id": 921, 
            "name": "10k_SAS", 
            "resource": "cinder.volume"
        }, 
        {
            "default_price": 1.0, 
            "default_threshold": 0.0, 
            "id": 1182, 
            "name": "network.tx", 
            "resource": "network.tx"
        }, 
        {
            "default_price": 0.002222, 
            "default_threshold": 150000.0, 
            "id": 1183, 
            "name": "network.rx", 
            "resource": "network.rx"
        }
    ]


GET /v1/project-info/<tenant_id>/
---------------------------------

Basic project info.

.. code-block:: bash

    majklk@samsung:~⟫ http http://10.10.10.100:9753/v1/project-info/18996ff490d240cab809419bdbfcbc78/                                                                                                                  
    HTTP/1.0 200 OK
    Content-Type: application/json
    Date: Thu, 01 Oct 2015 13:40:53 GMT
    Server: WSGIServer/0.1 Python/2.7.6

    {
        "customer_id": null, 
        "customer_name": null, 
        "extra": "{\"disk_7k2\": -1, \"disk_15k\": -1, \"memory\": 512000, \"disk_EasyTier\": -1, \"disk_10k\": -1, \"cpu\": 200}", 
        "id": 63, 
        "name": "tcp_lab_nwt", 
        "openstack_tenant": "18996ff490d240cab809419bdbfcbc78"
    }


GET /v1/server-list/<tenant_id>/<start_date>/<end_date>/
--------------------------------------------------------

.. code-block:: bash

    majklk@samsung:~⟫ http http://10.10.10.100:9753/v1/server-list/4a69b129bee3446b8e8b72d664777dc8/2015-8-10/2015-10-1/
    HTTP/1.0 200 OK
    Content-Type: application/json
    Date: Thu, 01 Oct 2015 13:49:06 GMT
    Server: WSGIServer/0.1 Python/2.7.6

    [
        {
            "active": true, 
            "name": "cfg01.int.mce.vpc.cloudlab.cz", 
            "network_in": "-", 
            "network_out": "-", 
            "price": 157.656425, 
            "storage_read": "-", 
            "storage_write": "-", 
            "type": "m1.large", 
            "uuid": "40076c5f-073e-48c6-936e-aac93ba14b0a", 
            "value": 24.983
        }, 
        {
            "active": true, 
            "name": "test300", 
            "network_in": "-", 
            "network_out": "-", 
            "price": 78.828213, 
            "storage_read": "-", 
            "storage_write": "-", 
            "type": "m1.medium", 
            "uuid": "2b02f77f-1a3f-4668-bca6-49e7b9368da6", 
            "value": 24.983
        }
    ]


GET /v1/address-list/<tenant_id>/<start_date>/<end_date>/
---------------------------------------------------------

Address List

.. code-block:: bash

    majklk@samsung:~⟫ http http://10.10.10.100:9753/v1/address-list/4a69b129bee3446b8e8b72d664777dc8/2015-8-10/2015-10-1/
    HTTP/1.0 200 OK
    Content-Type: application/json
    Date: Thu, 01 Oct 2015 13:51:18 GMT
    Server: WSGIServer/0.1 Python/2.7.6

    [
        {
            "active": true, 
            "name": "185.22.98.71", 
            "price": 24.983333, 
            "size": null, 
            "type": "ip", 
            "uuid": "2a753ba9-a974-44c3-b172-fa9ec0940b31", 
            "value": 24.983
        }
    ]

GET /v1/image-list/<tenant_id>/<start_date>/<end_date>/
-------------------------------------------------------

Image List

.. code-block:: bash

    majklk@samsung:~⟫ http http://10.10.10.100:9753/v1/image-list/4a69b129bee3446b8e8b72d664777dc8/2015-8-10/2015-10-1/
    HTTP/1.0 200 OK
    Content-Type: application/json
    Date: Thu, 01 Oct 2015 13:51:50 GMT
    Server: WSGIServer/0.1 Python/2.7.6

    [
        {
            "active": true, 
            "name": "junos", 
            "price": 0.0, 
            "size": 0, 
            "type": "Image", 
            "uuid": "8a095cc8-0ef4-4eba-8270-0c6690b11415", 
            "value": 25.0
        }
    ]

GET /v1/volume-list/<tenant_id>/<start_date>/<end_date>/
--------------------------------------------------------

.. code-block:: bash

    majklk@samsung:~⟫ http http://10.10.10.100:9753/v1/volume-list/4a69b129bee3446b8e8b72d664777dc8/2015-10-1/2015-10-1/
    HTTP/1.1 200 OK
    Connection: close
    Content-Type: application/json
    Date: Fri, 02 Oct 2015 10:17:53 GMT
    Server: gunicorn/18.0
    Transfer-Encoding: chunked

    [
        {
            "active": true, 
            "name": "mcevol", 
            "price": 0.195552, 
            "size": 10, 
            "type": "7k2_SAS", 
            "uuid": "4ad3fd5f-e465-4c74-9fc3-fb1093a512ee", 
            "value": 2.383
        }, 
        {
            "active": true, 
            "name": "mon01kedbmcevpccloudlabcz", 
            "price": 0.391105, 
            "size": 20, 
            "type": "7k2_SAS", 
            "uuid": "eddb3a06-1ddb-408c-bc5c-c14e18297a96", 
            "value": 2.383
        }, 
        {
            "active": true, 
            "name": "cfg01intmcevpccloudlabcz", 
            "price": 0.195552, 
            "size": 10, 
            "type": "7k2_SAS", 
            "uuid": "91f3b734-e4ff-4f9c-b0da-d098a46d2226", 
            "value": 2.383
        }, 
        {
            "active": true, 
            "name": "win", 
            "price": 0.586657, 
            "size": 30, 
            "type": "7k2_SAS", 
            "uuid": "7dbe6640-5c7c-469a-95bb-14d52fbf9636", 
            "value": 2.383
        }
    ]

GET /v1/network-list/<tenant_id>/<start_date>/<end_date>/
---------------------------------------------------------

.. warning::

    This works only if you have configured ``network`` tasks. 

.. note::

    All active instances has two resources with value and price calculated from rate and value if is over threshold.

.. code-block:: bash

    majklk@samsung:~⟫ http http://10.10.10.100:9753/v1/network-list/35391a2a80bc48958214ea1531f091f0/2015-8-1/2015-10-2/
    HTTP/1.0 200 OK
    Content-Type: application/json
    Date: Fri, 02 Oct 2015 11:32:26 GMT
    Server: WSGIServer/0.1 Python/2.7.6

    [
        {
            "active": true, 
            "name": "tcp_lab_mjk - tcp_lab_mjk : network.rx", 
            "price": 0.137156, 
            "size": null, 
            "type": "network.rx", 
            "uuid": "940cc555-5923-4f8d-b075-a349476cdfcb", 
            "value": 68578.0
        }, 
        {
            "active": true, 
            "name": "tcp_lab_mjk - tcp_lab_mjk : network.tx", 
            "price": 0.290608, 
            "size": null, 
            "type": "network.tx", 
            "uuid": "940cc555-5923-4f8d-b075-a349476cdfcb", 
            "value": 145304.0
        }, 
        {
            "active": true, 
            "name": "tcp_lab_mjk - tcp_lab_mjk : network.rx", 
            "price": 19.173888, 
            "size": null, 
            "type": "network.rx", 
            "uuid": "7b4510f4-55b3-439b-8b00-3d24bef291b8", 
            "value": 9586944.0
        }, 
        {
            "active": true, 
            "name": "tcp_lab_mjk - tcp_lab_mjk : network.tx", 
            "price": 13.1588, 
            "size": null, 
            "type": "network.tx", 
            "uuid": "7b4510f4-55b3-439b-8b00-3d24bef291b8", 
            "value": 6579400.0
        }
    ]

GET /v1/admin/rate-list/
------------------------

.. code-block:: bash

    majklk@samsung:~⟫ http http://10.10.10.100:9753/v1/admin/rate-list/
    HTTP/1.0 200 OK
    Content-Type: application/json
    Date: Fri, 02 Oct 2015 10:23:31 GMT
    Server: WSGIServer/0.1 Python/2.7.6

    [
        {
            "cinder.volume": 0.027383, 
            "glance.image": 0.002739, 
            "name": "adcstudio", 
            "network.rx": 0.002222, 
            "network.tx": 1.0, 
            "neutron.floating_ip": 1.0, 
            "nova.cpu": 0.821904, 
            "nova.instance": 12.620928, 
            "nova.memory": 0.000369, 
            "uuid": "c81a89366b204478a79153d2da14a5ce"
        }, 
        {
            "cinder.volume": 0.027383, 
            "glance.image": 0.002739, 
            "name": "admin", 
            "network.rx": 0.002222, 
            "network.tx": 1.0, 
            "neutron.floating_ip": 1.0, 
            "nova.cpu": 0.821904, 
            "nova.instance": 12.620928, 
            "nova.memory": 0.000369, 
            "uuid": "b1fe992b79904336a79a441dd6350569"
        }, 
    ]

Response 500
------------

.. code-block:: bash

    majklk@samsung:~⟫ http http://10.10.10.100:9753/v1/volume-list/35391a2a80bc48958214ea1531f091f0/2015-8-1/2015-10-2/
    HTTP/1.0 500 OK
    Content-Type: application/json
    Date: Fri, 02 Oct 2015 14:59:33 GMT
    Server: WSGIServer/0.1 Python/2.7.6

    {
        "error": "Unexpected Error. Please contact Administrator."
    }

.. note::

    For more information see Billometer log or check status in Sentry.

Response 301
------------

.. code-block:: bash

	HTTP/1.0 301 MOVED PERMANENTLY
	Content-Type: text/html; charset=utf-8
	Date: Fri, 02 Oct 2015 11:45:53 GMT
	Location: http://10.10.10.100:9753/v1/network-list/35391a2a80bc48958214ea1531f091f0/2015-8-1/2015-10-2
	Server: WSGIServer/0.1 Python/2.7.6

.. warning::

	Be sure that slash you have on end of your url.

Read more
---------

* http://django-openstack-auth.readthedocs.org/en/latest/
* http://django-rest-framework.org/
* http://docs.openstack.org/developer/python-ceilometerclient/
