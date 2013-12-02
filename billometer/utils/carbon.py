
from django.conf import settings

import socket
import time

def send_data(path, value):
    timestamp = int(time.time())
    sock = socket.socket()
#    sock.connect((settings.CARBON_SERVER, settings.CARBON_PORT))
    sock.connect(('10.0.103.159', 2023))
    sock.sendall('core_prod.%s %s %d\n' % (path, value, timestamp))
    sock.close()
