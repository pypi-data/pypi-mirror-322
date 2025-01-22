import unittest
from .middleware import generate_api_key, validate_api_key
from .config import configure_apikee

class TestApiKee(unittest.TestCase):
    def setUp(self):
        # Configure with a test secret
        configure_apikee({
            'secret': 'test-local-key'
        })

        # Generate API key before each test
        self.generated_keys = generate_api_key('key1')
        self.api_key = self.generated_keys['apiKey']
        self.key_id = self.generated_keys['keyId']

    def test_valid_local_api_key(self):
        # Test if the generated key is valid
        is_valid = validate_api_key(self.api_key, self.key_id)
        self.assertTrue(is_valid)

    def test_invalid_local_api_key(self):
        # Test if an invalid key is handled correctly
        is_valid = validate_api_key('invalid-key', self.key_id)
        self.assertFalse(is_valid)

if __name__ == '__main__':
    unittest.main()
