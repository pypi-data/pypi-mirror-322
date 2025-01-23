import os
import unittest

import pyKobana


class TestApiKobana(unittest.TestCase):
    def setUp(self):
        self.client = pyKobana.Kobana(os.getenv("KOBANA_ENV"), os.getenv("API_TOKEN"))

    def test_auth(self):
        response = self.client.getWallets()
        self.assertIsInstance(response, dict)

    def test_get(self):
        response = self.client.post("wallets", data={"key": "value"})
        self.assertIsInstance(response, dict)


if __name__ == "__main__":
    unittest.main()
