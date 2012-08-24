from twisted.trial import unittest

from twilix import errors
from twilix.stanzas import Iq
from twilix.jid import MyJID

from test import hostEmul, dispatcherEmul
from gateway import MyGatewayQuery, ClientGateway

class TestMyGatewayQuery(unittest.TestCase):

    def setUp(self):
        self.query = MyGatewayQuery(parent=Iq(from_='from', to='to',
                                              type_='get'),
                                    host=hostEmul(desc='desc',
                                                  prompt='prompt')
                                    )

    def test_getHandler(self):
        res = self.query.getHandler()
        host = self.query.host

        self.assertTrue(isinstance(res.parent, Iq))

        self.assertEqual(res.desc, host.desc)
        self.assertEqual(res.prompt, host.prompt)

        self.assertEqual(res.from_, self.query.to)
        self.assertEqual(res.to, self.query.from_)

    def test_setHandler(self):
        self.query.iq.type_ = 'set'
        self.query.prompt = 'jid'
        res = self.query.setHandler()
        jid = MyJID.escaped(self.query.prompt, self.query.iq.to)

        self.assertTrue(isinstance(res.parent, Iq))

        self.assertEqual(res.jid, jid)

        self.assertEqual(res.from_, self.query.to)
        self.assertEqual(res.to, self.query.from_)

class TestClientGateway(unittest.TestCase):

    def setUp(self):
        self.cg = ClientGateway(dispatcherEmul('jid'))

    def test_translateAddress(self):
        jid = 'client_jid'
        gateway = 'gateway'
        self.cg.translateAddress(jid, gateway)
        res = self.cg.dispatcher.data[0]

        self.assertTrue(isinstance(res, Iq))

        self.assertEqual(res.type_, 'set')
        self.assertEqual(res.to, MyJID(gateway))
        self.assertEqual(res.from_, self.cg.dispatcher.myjid)
