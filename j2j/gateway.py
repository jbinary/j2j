"""Module implements jabber:iq:gateway feature. (XEP-0100)

You can use this both to get JID's from other gateways and to
represent your gateway to others.
"""

from twilix.stanzas import Query, MyIq, Iq
from twilix import fields, errors
from twilix.disco import Feature
from twilix.jid import MyJID

xmlns = 'jabber:iq:gateway'

class GatewayQuery(Query):
    """
    Extends Query class.
    Base class for gateway queries.
    
    Attributes:
        desc -- string node 'desc' represents prompt text
        
        prompt -- string node 'prompt' represents the name of the 
        prompted item

        jid -- jid node 'jid' represents properly-formed jid
        based on the provided by the client
    """
    elementUri = xmlns
    result_class = 'self'

    desc = fields.StringNode('desc', required=False)
    prompt = fields.StringNode('prompt', required=False)
    jid = fields.JidNode('jid', required=False)

class MyGatewayQuery(GatewayQuery):
    """
    Extends GatewayQuery class.
    Define set/get handlers for gateway queries.
    """
    parentClass = MyIq

    def getHandler(self):
        """
        Calls from dispatcher when there is get gateway query.
        
        Returns iq stanza with gateway's info.
        """
        iq = self.iq.makeResult()
        query = GatewayQuery(desc=self.host.desc,
                             prompt=self.host.prompt,
                             parent=iq)
        return iq

    def setHandler(self):
        """
        Calls from dispatcher when there is set gateway query.
        
        Returns  iq stanza with the properly-formed jid
        based on the provided by the client.
        """
        escapedJID = MyJID.escaped(self.prompt, self.iq.to)
        iq = self.iq.makeResult()
        query = GatewayQuery(jid=escapedJID, parent=iq)
        return iq

class ClientGateway(object):
    """
    Gateway service class. Used to represent your own gateway to others and
    to ask other gateways.
    
    :param dispatcher: dispatcher instance to be used with the service.
    
    :param desc: prompt text
    
    :param prompt: name of the prompted item
    """
    def __init__(self, dispatcher, desc=None, prompt=None):
        """
        Sets gateway info and dispatcher value
        """
        self.dispatcher = dispatcher
        self.desc = desc
        self.prompt = prompt
        self.jid = None

    def init(self, disco=None):
        """
        Registers handlers and adds gateway feature in disco.
        Needs to be called if you want to represent your gateway to others.
        
        :param disco: client's disco instance.
        """
        self.dispatcher.registerHandler((MyGatewayQuery, self))

        if disco is not None:
            disco.root_info.addFeatures(Feature(var=xmlns))

    def translateAddress(self, clientID, gatewayJID, from_=None):
        """
        Makes set gateway query to some gateway
        
        :param clientID: id to translate.
        
        :param gatewayJID: sets the jid which will be used as translator.
        
        :param from_: sender for set gateway query (if differs from myjid)
        
        :returns:
            deferred object which waits for the result stanza
            with translated id
        """
        if from_ is None:
            from_ = self.dispatcher.myjid
        query = GatewayQuery(host=self,
                             prompt=clientID,
                             parent=Iq(type_='set', to=gatewayJID, from_=from_))
        self.dispatcher.send(query.iq)
        return query.iq.deferred
