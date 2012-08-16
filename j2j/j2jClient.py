from twisted.internet import reactor

from twilix.patterns.client import TwilixClient
from twilix.stanzas import Iq, Message, Presence
from twilix.base.myelement import EmptyStanza
from twilix.jid import MyJID

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

class HandlerMixIn(object):

    def anyHandler(self):
        to = self.host.ownerJID
        from_ = MyJID.escaped(self.from_.full(), self.host.transportJID)
        reply = self
        reply.from_ = from_
        reply.to = to
        self.host.transportDispatcher.send(reply)
        return EmptyStanza()

class IqHandler(HandlerMixIn, Iq):
    pass

class MessageHandler(HandlerMixIn, Message):
    pass

class j2jClient(TwilixClient):

    def __init__(self, initialPresence, *args, **kwargs):
        super(j2jClient, self).__init__(*args, **kwargs)
        self.transportDispatcher = initialPresence.host.dispatcher
        self.ownerJID = initialPresence.from_
        self.transportJID = initialPresence.host.myjid
        self.ownerStatus = None
        self.ownerPriority = None
        if initialPresence.status is not None and \
           initialPresence.priority is not None:
            self.ownerStatus = initialPresence.status
            self.ownerPriority = initialPresence.priority

    def init(self):
        self.f.maxRetries = 0
        self.dispatcher.registerHandler((IqHandler, self))
        self.dispatcher.registerHandler((MessageHandler, self))
        if self.ownerPriority is not None and self.ownerStatus is not None:
            reply = Presence()
            reply.status = self.ownerStatus
            reply.priority = self.ownerPriority
            self.dispatcher.send(reply)

    def disconnect(self):
        self.xmlstream.sendFooter()
        reactor.callLater(10, self.connector.disconnect)
