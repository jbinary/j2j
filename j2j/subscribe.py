from twilix.stanzas import Presence
from twilix.base.myelement import EmptyStanza

class SubscrHandler(Presence):

    def probeHandler(self):
        reply = self.get_reply()
        reply.to = reply.to.bare()
        reply.type_ = 'probe'
        return reply

    def subscribeHandler(self):
        reply1 = self.get_reply()
        reply1.type_ = 'subscribed'
        return reply1, self.probeHandler()

    def availableHandler(self):
        return self.get_reply()

    def unavailableHandler(self):
        reply = self.get_reply()
        reply.type_ = 'unavailable'
        return reply

    def subscribedHandler(self):
        return EmptyStanza()

    def unsubscribedHandler(self):
        reply = Presence(to=self.from_, from_=self.to, type_='unsubscribed')
        return reply
