import unittest
from main import app, load_cbr_rates

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index_get(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'USD', response.data)
        self.assertIn(b'EUR', response.data)

    def test_index_post(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(usd_amount='100', eur_amount='200'))
        self.assertEqual(response.status_code, 200)

    def test_load_cbr_rates(self):
        cbr_rates = load_cbr_rates()
        self.assertIsNotNone(cbr_rates)
        self.assertIsInstance(cbr_rates, dict)
        self.assertIn('USD', cbr_rates)
        self.assertIn('EUR', cbr_rates)
        self.assertIsInstance(cbr_rates['USD'], float)
        self.assertIsInstance(cbr_rates['EUR'], float)

if __name__ == '__main__':
    unittest.main()
