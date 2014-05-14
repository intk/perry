import sys
import socket
import uuid

from twisted.internet import reactor
from twisted.application import service, internet
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint

from twisted.python import log
log.startLogging(sys.stdout)

from discovery import DiscoveryProtocol
from control import ControlConnectionFactory
from registry import ConnectionRegistry

from settings import *

import utils

details = utils.Details(MY_UID, MY_NAME)
host = utils.get_localhost_ip()

registry = ConnectionRegistry()

reactor.listenMulticast(DISCOVERY_PORT, DiscoveryProtocol(host, DISCOVERY_PORT, registry.new_discovery), listenMultiple=True)

factory = ControlConnectionFactory.get(details, registry.new_connection, registry.connection_lost)
control_interface = TCP4ServerEndpoint(reactor, DATA_PORT)
control_interface.listen(factory)

registry.control_factory = factory

reactor.run()
