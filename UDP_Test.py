import socket
import sys
import numpy as np
import random


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('127.0.0.1', 5678)
message = str(random.randint(1,101)) + ' 51'

while 1:
    try:

        # Send data
        sent = sock.sendto(message, server_address)

        # Receive response
        #print >>sys.stderr, 'waiting to receive'
        data, server = sock.recvfrom(4096)
        print data
        #print >>sys.stderr, 'received "%s"' % data

    finally:
        pass
        #print >>sys.stderr, 'closing socket'
        #sock.close()
