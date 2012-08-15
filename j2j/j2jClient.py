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
        to = self.host.hostJID
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

class PresenceHandler(Presence):

    def availableHandler(self):
        # from = dtest.hidevlab.com
        # to = transport_test@jabb3r.org/res
        # redirect answer to dmitry@hidevlab.com
        to = self.host.hostJID
        from_ = MyJID.escaped(self.to.full(), self.host.transportJID)
        reply = self.get_reply()
        reply.to = to
        reply.from_ = from_
        self.host.transportDispatcher.send(reply)
        return EmptyStanza()

class j2jClient(TwilixClient):

    def __init__(self, transportDispatcher, *args, **kwargs):
        super(j2jClient, self).__init__(*args, **kwargs)
        self.transportDispatcher = transportDispatcher

    def init(self):
        self.f.maxRetries = 0
        self.hostJID = None
        self.transportJID = None
        self.dispatcher.registerHandler((IqHandler, self))
        self.dispatcher.registerHandler((MessageHandler, self))
        self.dispatcher.registerHandler((PresenceHandler, self))

    def disconnect(self):
        self.xmlstream.sendFooter()
        reactor.callLater(10, self.connector.disconnect)
