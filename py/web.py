import sys
import json

from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web import http

class StaticHandler(Resource):

    isLeaf = True

    def render_GET(self, request):
        path = request.postpath[0]
        return open("./static/" + path, "r").read()


class DataHandler(Resource):

    isLeaf = True

    def __init__(self, registry):
        Resource.__init__(self)
        self.registry = registry

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

def get_site(registry):
    root = Resource()
    root.putChild("static", StaticHandler())
    root.putChild("data", DataHandler(registry))
    return Site(root, timeout=None)
