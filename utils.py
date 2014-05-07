import os
import socket
import hashlib
import uuid

def get_current_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #gethostbyname(gethostname())
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip



def get_sample_data():

    for i in range(0, 10):
        random_data = uuid.uuid4()
        yield hashlib.sha1(random_data).hexdigest()

