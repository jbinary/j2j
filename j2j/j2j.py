import time
import os

from twisted.internet import task
from twisted.internet.defer import Deferred

from twilix.stanzas import Message, Presence, Iq
from twilix.base.exceptions import WrongElement
from twilix.version import ClientVersion
import twilix.disco as disco
from twilix.patterns.component import TwilixComponent

from twilix.vcard import VCard, VCardQuery
from myvcard import WeatherVCardQuery, WeatherVersionQuery

from presence import MyPresence

class j2jComponent(TwilixComponent):
    def __init__(self, version, config, cJid):
        TwilixComponent.__init__(self, cJid)
        self.config = config
        self.VERSION = version
        self.startTime = None
        self.subscribed = SubscribedList(config)
        self.online = []           

    def init(self):
        self.startTime = time.time()
        self.dispatcher.registerHandler((MyPresence, self))
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
        self.disco.init()
        self.getOnline()
        #self.lc = task.LoopingCall(self.updateStatus)
        #self.lc.start(900)
        print 'Connected!'
"""
    def addSubscr(self, from_, to):
        self.subscribed.add_subscr(from_, to)
    
    def rmSubscr(self, from_, to):
        self.subscribed.rm_subscr(from_, to)
    
    def addOnlinesubscr(self, from_, to):
        if (from_, to) not in self.online:
            self.online.append((from_, to))
            
    def rmOnlinesubscr(self, from_, to):
        if (from_, to) in self.online:
            self.online.remove((from_, to))
    
    def getOnline(self):
        for from_, to in self.subscribed.subscr_list:
            reply = Presence(
                          to=from_,
                          from_=to,
                          type_='probe',                          
                        )
            self.dispatcher.send(reply)
    
    def _result(self, respond, from_, to):
        reply = Presence(
                          to=from_,
                          from_=to,
                          status=respond,                          
                        )
        self.dispatcher.send(reply)
        """
