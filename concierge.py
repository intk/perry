import sys
import socket
import uuid

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.python import log
from twisted.internet.task import LoopingCall

from neighbours import Neighbour

class Concierge(DatagramProtocol):
    CMD_PING = "magic-ping"
    CMD_PONG = "magic-pong"

    DISCOVERY_INVERVAL = 1 # sec

    def __init__(self, host, port, new_neighbour_callback=None):
        self.host = host
        self.port = port
        self.new_neighbour_callback = new_neighbour_callback

    def startProtocol(self):
        self.transport.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

        self.periodic_shout = LoopingCall(self.sendDatagram)
        self.periodic_shout.start(self.DISCOVERY_INVERVAL)


    def sendDatagram(self):
        log.msg("sending discovery datagram")
        self.transport.write(self.CMD_PING, ('255.255.255.255', self.port)) # <- write to broadcast address here

    def datagramReceived(self, datagram, address):

        if address[0] == self.host:
            #log.msg("Received own announcement: datagram=%s, address=%s" % (datagram, address))
            return

        log.msg("Datagram %s received from %s" % (datagram, address))

        if datagram.startswith(self.CMD_PING):
            # someone publishes itself, we reply that we are here
            self.transport.write(self.CMD_PONG, address)
        elif datagram.startswith(self.CMD_PONG):
            # someone reply to our publish message

            #FIXME: dummy neighbour hash generation
            self.new_neighbour_callback(Neighbour(str(uuid.uuid4()), address[0]))
            log.msg("Got client: %s, %s" % (address[0], address[1]))

