import sys
import uuid

from twisted.internet.protocol import DatagramProtocol

from twisted.python import log

from twisted.internet.task import LoopingCall
from twisted.application.internet import MulticastServer


class DiscoveryProtocol(DatagramProtocol):

    CMD_PING = "magic-ping"
    CMD_PONG = "magic-pong"

    GROUP = "239.255.5.5"

    ANNOUNCE_INVERVAL = 5 # sec

    def __init__(self, host, port, callback):
        self.host = host
        self.port = port
        self.callback = callback

    def startProtocol(self):

        #239.255.0.0 - 239.255.255.255
        self.transport.joinGroup(self.GROUP)

        #self.transport.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

        self.periodic_shout = LoopingCall(self.sendDatagram)
        self.periodic_shout.start(self.ANNOUNCE_INVERVAL)


    def sendDatagram(self):
        log.msg("sending discovery datagram")
        self.transport.write(self.CMD_PING, (self.GROUP, self.port))


    def datagramReceived(self, datagram, address):

        log.msg("Datagram %s received from %s" % (datagram, address))

        if address[0] == self.host:
            log.msg("Received own announcement: datagram=%s, address=%s" % (datagram, address))
            return

        if datagram.startswith(self.CMD_PING):
            # someone publishes itself, we reply that we are here
            self.transport.write(self.CMD_PONG, address)
        elif datagram.startswith(self.CMD_PONG):
            # someone is announcing himself

            log.msg("Got possible client: %s, %s" % address)
            self.callback(address)





