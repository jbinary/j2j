import time

from twisted.internet.defer import Deferred

from twilix.stanzas import Presence, Message
from twilix.version import ClientVersion
from twilix.disco import Disco
from twilix.patterns.component import TwilixComponent
from twilix.dispatcher import Dispatcher

from twilix.vcard import VCard, VCardQuery
from twilix.register import Register
from registration import RegisterHandler
from subscribe import SubscrHandler, PresenceHandler
from j2jClient import ClientPool
from gateway import ClientGateway

class j2jComponent(TwilixComponent):
    """
    Master class for the jabber-to-jabber service.
    """
    def __init__(self, version, jid, basepath, basetype):
        """
        Sets info about transport.
        
        :param version: version of your transport.
        
        :param jid: jid of your transport.
        
        :param basepath: path to your users database.
        
        :param basetype: type of your users database
        """
        TwilixComponent.__init__(self, jid)
        self.config = config
        self.VERSION = version
        self.startTime = None
        self.basetype = basetype
        _tmp = __import__('%sBase' % basetype, globals(), locals(),
                                                    ['UserBase'], -1)
        self.dbase = _tmp.UserBase(basepath)
        self.pool = ClientPool()

    def init(self):
        """
        Method initializing all needed services and handlers.
        """
        self.startTime = time.time()
        self.dispatcher.registerHandler((Presence, self))
        self.dispatcher.registerHandler((Message, self))
        self.dispatcher.registerHandler((SubscrHandler, self))
        self.dispatcher.registerHandler((PresenceHandler, self))
        self.disco = Disco(self.dispatcher)
        self.version = ClientVersion(self.dispatcher,
                                    'j2j transport',
                                    self.VERSION, 'Linux')
        self.version.init(self.disco)
        self.myvcard = VCardQuery(nickname='j2j',
                                  jid=self.myjid,
                                  description='\
Jabber to jabber gateway')
        self.vcard = VCard(self.dispatcher, myvcard=self.myvcard)
        self.vcard.init(self.disco)
        self.register = Register(self.dispatcher)
        self.register.init((RegisterHandler, self), self.disco)
        self.gateway = ClientGateway(self.dispatcher,
                                     'Please enter the Jabber Screen Name of \
the person you would like to contact',
                                     'Contact ID')
        self.gateway.init(self.disco)
        self.disco.init()
        print 'Connected!'

    def componentDisconnected(self):
        """
        If type of your database is 'shelve', this method will close
        your database properly.
        """
        if self.basetype == 'shelve':
            self.dbase.close()
