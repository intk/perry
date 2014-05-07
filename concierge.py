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

    def __init__(self, host, port, new_neighbour_callback=None):
        self.host = host
        self.port = port
        self.new_neighbour_callback = new_neighbour_callback

    def startProtocol(self):
        # Set the TTL>1 so multicast will cross router hops:
        #self.transport.setTTL(5)

        self.transport.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

        #self.periodic_shout = LoopingCall(self.sendDatagram)
        #self.periodic_shout.start(1)


    def sendDatagram(self):
        log.msg("sending discovery datagram")
        self.transport.write(self.CMD_PING, ('255.255.255.255', self.port)) # <- write to broadcast address here
        #self.transport.write(self.CMD_PING, self.MULTICAST_ADDR)

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
            self.new_neighbour_callback(Neighbour(str(uuid.uuid4()), address[0]))
            log.msg("Got client: %s, %s" % (address[0], address[1]))

