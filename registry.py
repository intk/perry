from twisted.python import log
from twisted.internet import defer, reactor

from control import connect
from settings import *


class ConnectionRegistry(object):

    def __init__(self):

        self.control_connections = []
        self.data_connections = []

    def new_discovery(self, address):
        log.msg("Discovery callback called with args=%s" % (address,))

        host = address[0]
        d = connect(self.control_factory, host, DATA_PORT)
#        attempt = myEndpoint.connect(myFactory)
#        reactor.callLater(30, attempt.cancel)
        #d.addCallback(self.new_connection)

    def new_connection(self, protocol):
        log.msg("Connection created, self=%s" % self, system="ConnectionRegistry")
        self.control_connections.append(protocol)

        log.msg("%d connections" % len(self.control_connections))

        d1 = defer.Deferred()
        d1.addCallback(lambda p : p.remoteGetDetails())
        d1.addErrback(self.someError)
        
        d2 = defer.Deferred()
        d2.addCallback(lambda p: p.remoteGetShared())
        d2.addErrback(self.someError)

        d3 = defer.DeferredList([d1, d2], fireOnOneErrback=True) #consumeErrors=True, 

        d3.addCallback(self.handshakeDone)
        d3.addErrback(self.someError)

        reactor.callLater(1, d1.callback, protocol)
        reactor.callLater(1, d2.callback, protocol)



    def connection_lost(self, protocol):
        log.msg("AMP connection lost")
        self.control_connections.remove(protocol)

    def handshakeDone(self, results):
        log.msg("Handshake done! results=%s" % (results,))

    def someError(self, failure):
        log.err("Error! %s" % failure)
        return failure
