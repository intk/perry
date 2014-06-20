import sys
import json
import socket
from twisted.python import log

log.startLogging(sys.stdout)

class Neighbour(object):

    def __init__(self, nhash, host):
        self.nhash = nhash
        self.host = host

    def get_shared(self):
        return ["asdaD", "ertert"]

    def to_dict(self):
        return dict(nhash=self.nhash, host=self.host)

    def __repr__(self):
        return "Neighbour(nhash=%s, host=%s)" % (self.nhash, self.host)


