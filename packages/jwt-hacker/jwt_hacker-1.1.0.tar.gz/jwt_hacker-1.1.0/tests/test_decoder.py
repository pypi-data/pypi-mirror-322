import unittest
import base64
from jwt_hacker.decoder import *

class TestDecoder(unittest.TestCase):
    def test_decode_base64(self):
        self.assertEqual(decode_base64("SGVsbG8="), "Hello")
        self.assertIsNone(decode_base64("InvalidBase64"))

    def test_decode_base58(self):
        self.assertEqual(decode_base58("StV1DL6CwTryKyV"), "Hello world")  # Matches the output case
        self.assertIsNone(decode_base58("InvalidBase58"))

    def test_decode_rot13(self):
        self.assertEqual(decode_rot13("Hello"), "Uryyb")
        self.assertEqual(decode_rot13("Uryyb"), "Hello")

    def test_decode_gzip(self):
        compressed = base64.b64encode(gzip.compress(b"Hello")).decode()
        self.assertEqual(decompress_gzip(compressed), "Hello")
        self.assertIsNone(decompress_gzip("InvalidGzip"))

    def test_decode_hex(self):
        self.assertEqual(decode_hex("48656c6c6f"), "Hello")
        self.assertIsNone(decode_hex("InvalidHex"))

    def test_decode_binary(self):
        self.assertEqual(decode_binary("0100100001100101011011000110110001101111"), "Hello")
        self.assertIsNone(decode_binary("InvalidBinary"))

    def test_decode_url(self):
        self.assertEqual(decode_url("Hello%20World"), "Hello World")
        self.assertIsNone(decode_url(None))

    def test_decode_ascii85(self):
        # Valid input encoded with Ascii85
        self.assertEqual(decode_ascii85("<~87cURD_*#TDfTZ)+T~>"), "Hello, world!")
        # Invalid input
        self.assertIsNone(decode_ascii85("InvalidAscii85"))

    def test_decode_base32(self):
        self.assertEqual(decode_base32("JBSWY3DP"), "Hello")
        self.assertIsNone(decode_base32("InvalidBase32"))

    def test_hash_md5(self):
        self.assertEqual(hash_md5("test"), hashlib.md5(b"test").hexdigest())

if __name__ == "__main__":
    unittest.main()
