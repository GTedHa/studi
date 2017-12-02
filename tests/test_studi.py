import unittest

import studi


class StudiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = studi.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to Studi', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
