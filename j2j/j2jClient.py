from twisted.internet import reactor

from twilix.patterns.client import TwilixClient

class WrongClientException(Exception):
    pass

class DuplicateClientsException(Exception):
    pass

class ClientPool(object):

    def __init__(self):
        self.pool = {}

    def addClient(self, jid, client):
        if jid not in self.pool.keys():
            self.pool[jid] = client
        else:
            raise DuplicateClientsException

    def removeClient(self, jid):
        if jid in self.pool.keys():
            self.pool.pop(jid)
        else:
            raise WrongClientException

class j2jClient(TwilixClient):

    def init(self):
        self.f.maxRetries = 0

    def disconnect(self):
        self.xmlstream.sendFooter()
        reactor.callLater(10, self.connector.disconnect)
