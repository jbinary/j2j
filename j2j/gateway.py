from twilix.stanzas import Query, MyIq, Iq
from twilix import fields, errors
from twilix.disco import Feature
from twilix.jid import MyJID

xmlns = 'jabber:iq:gateway'

class GatewayQuery(Query):
    elementUri = xmlns
    result_class = 'self'

    desc = fields.StringNode('desc', required=False)
    prompt = fields.StringNode('prompt', required=False)
    jid = fields.JidNode('jid', required=False)

class MyGatewayQuery(GatewayQuery):
    parentClass = MyIq

    def getHandler(self):
        iq = self.iq.makeResult()
        query = GatewayQuery(desc=self.host.desc,
                             prompt=self.host.prompt,
                             parent=iq)
        return iq

    def setHandler(self):
        escapedJID = MyJID.escaped(self.prompt, self.iq.to)
        iq = self.iq.makeResult()
        query = GatewayQuery(jid=escapedJID, parent=iq)
        return iq

class ClientGateway(object):
    def __init__(self, dispatcher, desc=None, prompt=None):
        self.dispatcher = dispatcher
        self.desc = desc
        self.prompt = prompt
        self.jid = None

    def init(self, disco=None):
        self.dispatcher.registerHandler((MyGatewayQuery, self))

        if disco is not None:
            disco.root_info.addFeatures(Feature(var=xmlns))

    def translateAddress(self, clientJID, gatewayJID, from_=None):
        if from_ is None:
            from_ = self.dispatcher.myjid
        query = GatewayQuery(host=self,
                             prompt=clientJID,
                             parent=Iq(type_='set', to=gatewayJID, from_=from_))
        self.dispatcher.send(query.iq)
        return query.iq.deferred
