from tastypie.test import ResourceTestCase

__author__ = 'ericqu'


class P4ClientResourceTest(ResourceTestCase):

    def setUp(self):
        self.username = 'equ'
        self.password = '412D4441E4DD93EDF3259AF13115CDEB'

    def get_credentials(self):
        return 'p4ticket %s:%s' % (self.username, self.password)

    def test_delete_client(self):
        self.assertHttpOK(self.api_client.delete('/api/p4/client/equ_P4CM_WEB_yDExSd/'))
