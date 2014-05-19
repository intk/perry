import sys
import json
from twisted.protocols.amp import AMP
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint, TCP4ClientEndpoint
from twisted.application.service import Application
from twisted.application.internet import StreamServerEndpointService

from twisted.python import log

from twisted.protocols.amp import Integer, String, Unicode, Command
from twisted.protocols.amp import CommandLocator


class IncorrectUID(Exception):
    pass


class GetDetails(Command):
    arguments = [('uid', String())]         # + pgp key id
    response = [('uid', String()), ('name', String())]
    errors = {IncorrectUID: 'incorrect-uid'}

class GetShared(Command):
    arguments = [('uid', String())]         # + pgp key id
    response = [('shared', String())]
    errors = {IncorrectUID: 'incorrect-uid'}


class ControlProtocol(AMP):

    def __init__(self, details, new_connection_callback, connection_lost_callback):
        AMP.__init__(self)
        self.details = details
        self.new_connection_callback = new_connection_callback
        self.connection_lost_callback = connection_lost_callback

    @GetDetails.responder
    def get_details(self, uid):
        log.msg("Get details request from %s" % uid, system="ControlProtocol.get_details")

        if not uid:
            raise IncorrectUID()

        return dict(uid=self.details.uid, name=self.details.name)

    @GetShared.responder
    def get_shared(self, uid):
        log.msg("Get shared request from %s" % uid, system="ControlProtocol.get_shared")

        if not uid:
            raise IncorrectUID()

        return dict(shared=json.dumps(["somefile-to-%s" % uid, "anotherfile-to-%s" % uid]))

    def connectionMade(self):
        self.new_connection_callback(self)

    def connectionLost(self, reason):
        self.connection_lost_callback(self)
        return AMP.connectionLost(self, reason)

    def remoteGetDetails(self):
        return self.callRemote(
            GetDetails,
            uid = self.details.uid
        )

    def remoteGetShared(self):
        return self.callRemote(
            GetShared,
            uid = self.details.uid
        )


class ControlConnectionFactory(Factory):

    @staticmethod
    def get(details, new_connection, connection_lost):
        f = ControlConnectionFactory()
        f.protocol = lambda: ControlProtocol(details, new_connection, connection_lost)
        return f

    def connect(self, host, port):
        return TCP4ClientEndpoint(reactor, host, port).connect(self)


