import unittest
from jwt_hacker.decoder import operations

class TestIntegration(unittest.TestCase):
    def test_jwt_header_decoding(self):
        # Example JWT header (Base64-encoded)
        header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        expected_output = '{"alg":"HS256","typ":"JWT"}'
        self.assertEqual(operations["Base64"](header), expected_output)

    def test_jwt_payload_decoding(self):
        # Example JWT payload (Base64-encoded)
        payload = "eyJ1c2VyIjoiam9obmRvZSIsInJvbGUiOiJhZG1pbiJ9"
        expected_output = '{"user":"johndoe","role":"admin"}'
        self.assertEqual(operations["Base64"](payload), expected_output)

if __name__ == "__main__":
    unittest.main()
