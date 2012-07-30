import time
import os

from twisted.internet import task
from twisted.internet.defer import Deferred

from twilix.stanzas import Message, Presence, Iq
from twilix.base.exceptions import WrongElement
from twilix.version import ClientVersion
import twilix.disco as disco
from twilix.patterns.component import TwilixComponent
from twilix.dispatcher import Dispatcher
from registration import RegisterHandler
from twilix.register import Register

from twilix.vcard import VCard, VCardQuery

class j2jComponent(TwilixComponent):
    def __init__(self, version, config, cJid):
        TwilixComponent.__init__(self, cJid)
        self.config = config
        self.VERSION = version
        self.startTime = None

    def componentConnected(self, xs):
        self.startTime = time.time()
        self.dispatcher = Dispatcher(xs, self.myjid)
        self.dispatcher.registerHandler((Presence, self))
        self.dispatcher.registerHandler((Message, self))
        self.disco = disco.Disco(self.dispatcher)
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
