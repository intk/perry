from twisted.python import log
from twisted.internet import defer, reactor

from settings import *


class ConnectionRegistry(object):

    def __init__(self):

        self.pre_connections = []
        self.control_connections = []
        self.data_connections = []

    def new_discovery(self, address):
        log.msg("Discovery callback called with args=%s" % (address,))

        host = address[0]

        self.control_factory.connect(host, DATA_PORT)

    def new_connection(self, protocol):
        log.msg("Connection created, asking for details, self=%s" % self)
        self.pre_connections.append(protocol)

        d1 = defer.Deferred()
        d1.addCallback(lambda p : p.remoteGetDetails())
        #d1.addErrback(self.someError)
        
        d2 = defer.Deferred()
        d2.addCallback(lambda p: p.remoteGetShared())

        d3 = defer.DeferredList([d1, d2], fireOnOneErrback=True) #consumeErrors=True, 

        d3.addCallback(self.handshakeDone)
        d3.addErrback(lambda f: self.cantFinishHandshake(protocol, f))

        reactor.callLater(1, d1.callback, protocol)
        reactor.callLater(1, d2.callback, protocol)



    def connection_lost(self, protocol):
        log.msg("AMP connection lost")
        self.control_connections.remove(protocol)


    def handshakeDone(self, results):
        log.msg("Handshake done! results=%s" % (results,))

        self.pre_connections.remove(protocol)
        self.control_connections.remove(protocol)


    def cantFinishHandshake(self, protocol, failure):
        self.pre_connections.remove(protocol)
        log.err("Error! %s" % failure)
        return failure



