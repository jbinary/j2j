from twilix.stanzas import Query, MyIq, Iq
from twilix import fields, errors
from twilix.disco import Feature
from twilix.jid import MyJID

xmlns = 'jabber:iq:gateway'

class GatewayQuery(Query):
    elementUri = xmlns

    desc = fields.StringNode('desc', required=False)
    prompt = fields.StringNode('prompt', required=False)

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
        query = GatewayQuery(parent=iq)
        jid = query.addElement('jid')
        jid.addChild(escapedJID.full())
        return iq

class ClientGateway(object):
    def __init__(self, dispatcher, desc=None, prompt=None):
        self.dispatcher = dispatcher
        self.desc = desc
        self.prompt = prompt

    def init(self, disco=None):
        self.dispatcher.registerHandler((MyGatewayQuery, self))

        if disco is not None:
            disco.root_info.addFeatures(Feature(var=xmlns))
