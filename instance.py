import sys
import json

from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web import http
from twisted.internet import reactor, defer
from twisted.python import log


from concierge import Concierge
from utils import get_current_ip, get_sample_data

PORT = 50000

DATA = get_sample_data()

MY_HASH = 'e4fdd677-e34f-4e8f-bec2-725b7bc6def0'

class StaticHandler(Resource):

    isLeaf = True

    def render_GET(self, request):
        path = request.postpath[0]
        return open("./static/" + path, "r").read()

class DataHandler(Resource):

    isLeaf = True

    def __init__(self, neighbours):
        Resource.__init__(self)
        self.neighbours = neighbours

    def render_GET(self, request):
        node = request.postpath[0]

        if node == "neighbours":
            data = [n.to_dict() for n in self.neighbours.values()]
        elif node == "my-hash":
            data = dict(myhash=MY_HASH)
        elif node == "my-data":
            data = dict(mydata=DATA)
        elif node == "neighbour-data":
            nid = request.postpath[1]
            data = self.neighbours[nid].get_shared()

        return json.dumps(data)

if __name__ == '__main__':

    ip = get_current_ip()

    neighbours = {}
    def add_new_neighbour(n):
        log.msg("New neighbour %s, hello!" % n)
        neighbours[n.nhash] = n

    concierge = Concierge(ip, PORT, new_neighbour_callback=add_new_neighbour)


    root = Resource()
    root.putChild("static", StaticHandler())
    root.putChild("data", DataHandler(neighbours))

    site = Site(root, timeout=None)

    reactor.listenUDP(PORT, concierge)
    reactor.listenTCP(8080, site)


    reactor.run()

