import unittest

from twisted.words.protocols.jabber.jid import JID

from twilix import errors
from twilix.stanzas import Iq

from j2j.test import hostEmul, dispatcherEmul
