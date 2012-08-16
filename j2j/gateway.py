from twilix.stanzas import Query, MyIq, Iq
from twilix.disco import Feature
from twilix import fields, errors

class GatewayQuery(Query):
    elementUri = 'jabber::iq::gateway'

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
        raise errors.BadRequestException()

class ClientGateway(object):
    def __init__(self, dispatcher, desc=None, prompt=None):
        self.dispatcher = dispatcher
        self.desc = desc
        self.prompt = prompt

    def init(self, disco=None, handlers=None):
        self.dispatcher.registerHandler((MyGatewayQuery, self))
        if handlers is None:
            handlers = ()
        for handler, host in handlers:
            self.dispatcher.registerHandler((handler, host))

        if disco is not None:
            disco.root_info.addFeatures(Feature(var='jabber::iq::gateway'))
