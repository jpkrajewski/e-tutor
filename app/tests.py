from django.test import TestCase, SimpleTestCase
from django.conf import settings


class RunTest(SimpleTestCase):
    def test_debug_mode(self):
        """
        Debug must be set to False
        """

        self.assertEqual(settings.DEBUG, False)
    
    
