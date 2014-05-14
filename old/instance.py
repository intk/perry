import sys
import json

from twisted.internet import reactor, defer
from twisted.python import log

from . import web

from utils import get_sample_data

DATA = get_sample_data()

MY_HASH = 'e4fdd677-e34f-4e8f-bec2-725b7bc6def0'


if __name__ == '__main__':




    reactor.listenUDP(PORT, concierge)
    reactor.listenTCP(8080, web.get_site())


    reactor.run()

