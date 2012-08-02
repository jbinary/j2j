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
from dbase import UserBase
from j2jClient import ClientPool

class j2jComponent(TwilixComponent):
    def __init__(self, version, config, cJid, basepath):
        TwilixComponent.__init__(self, cJid)
        self.config = config
        self.VERSION = version
        self.startTime = None
        self.dbase = UserBase(basepath)
        self.pool = ClientPool()

    def init(self):
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
        self.disco.init()
        print 'Connected!'

    def componentDisconnected(self):
        self.dbase.close()
