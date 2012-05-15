from django.test import TestCase
from django.test.utils import override_settings

from rq.job import Job

from .queues import get_connection, get_queue


TEST_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    'test': {
        'HOST': 'localhost',
        'PORT': 1,
        'DB': 1,
    }
}


class DjangoRQTest(TestCase):

    @override_settings(RQ_QUEUES=TEST_QUEUES)
    def test_get_connection(self):
        """
        Test that get_connection returns the right connection based on 
        settings.RQ_QUEUES
        """
        config = TEST_QUEUES['default']
        connection = get_connection()
        connection_kwargs = connection.connection_pool.connection_kwargs
        self.assertEqual(connection_kwargs['host'], config['HOST'])
        self.assertEqual(connection_kwargs['port'], config['PORT'])
        self.assertEqual(connection_kwargs['db'], config['DB'])

        config = TEST_QUEUES['test']
        connection = get_connection('test')
        connection_kwargs = connection.connection_pool.connection_kwargs
        self.assertEqual(connection_kwargs['host'], config['HOST'])
        self.assertEqual(connection_kwargs['port'], config['PORT'])
        self.assertEqual(connection_kwargs['db'], config['DB'])

    @override_settings(RQ_QUEUES=TEST_QUEUES)
    def test_get_queue(self):
        # Test that get_queue use the right parameters for its connection
        config = TEST_QUEUES['default']
        queue = get_queue('default')
        connection_kwargs = queue.connection.connection_pool.connection_kwargs
        self.assertEqual(queue.name, 'default')
        self.assertEqual(connection_kwargs['host'], config['HOST'])
        self.assertEqual(connection_kwargs['port'], config['PORT'])
        self.assertEqual(connection_kwargs['db'], config['DB'])

        config = TEST_QUEUES['test']
        queue = get_queue('test')
        connection_kwargs = queue.connection.connection_pool.connection_kwargs
        self.assertEqual(queue.name, 'test')
        self.assertEqual(connection_kwargs['host'], config['HOST'])
        self.assertEqual(connection_kwargs['port'], config['PORT'])
        self.assertEqual(connection_kwargs['db'], config['DB'])
