import unittest
import base64
import hashlib
import gzip
import hmac
import zlib
import codecs
import binascii
from jwt_hacker.decoder import (
    decode_base64,
    decode_base32,
    decode_base58,
    decode_ascii85,
    decode_binary,
    decode_hex,
    decode_url,
    decode_rot13,
    decompress_gzip,
    decompress_zlib,
    hash_md5,
    hash_sha1,
    hash_sha256,
    hash_sha512,
    hash_sha3_256,
    hash_sha3_512,
    verify_hs256,
    verify_rs256,
    verify_ps256,
    verify_ecdsa,
    aes_cbc_decrypt,
    aes_gcm_decrypt
)
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.kdf.argon2 import Argon2


class TestDecoder(unittest.TestCase):

    # BASE DECODING FUNCTIONS
    def test_decode_base64(self):
        self.assertEqual(decode_base64("SGVsbG8="), "Hello")
        self.assertIsNone(decode_base64("InvalidBase64"))

    def test_decode_base32(self):
        self.assertEqual(decode_base32("JBSWY3DP"), "Hello")
        self.assertIsNone(decode_base32("InvalidBase32"))

    def test_decode_base58(self):
        self.assertEqual(decode_base58("StV1DL6CwTryKyV"), "Hello world")
        self.assertIsNone(decode_base58("InvalidBase58"))

    def test_decode_ascii85(self):
        self.assertEqual(decode_ascii85("<~87cURD_*#TDfTZ)+T~>"), "Hello, world!")
        self.assertIsNone(decode_ascii85("InvalidAscii85"))

    # HASHING FUNCTIONS
    def test_hash_md5(self):
        self.assertEqual(hash_md5("test"), hashlib.md5(b"test").hexdigest())

    def test_hash_sha1(self):
        self.assertEqual(hash_sha1("test"), hashlib.sha1(b"test").hexdigest())

    def test_hash_sha256(self):
        self.assertEqual(hash_sha256("test"), hashlib.sha256(b"test").hexdigest())

    def test_hash_sha512(self):
        self.assertEqual(hash_sha512("test"), hashlib.sha512(b"test").hexdigest())

    def test_hash_sha3_256(self):
        self.assertEqual(hash_sha3_256("test"), hashlib.sha3_256(b"test").hexdigest())

    def test_hash_sha3_512(self):
        self.assertEqual(hash_sha3_512("test"), hashlib.sha3_512(b"test").hexdigest())

    # JWT VERIFICATION FUNCTIONS
    def test_verify_hs256(self):
        header = base64.urlsafe_b64encode(b'{"alg":"HS256","typ":"JWT"}').decode().rstrip("=")
        payload = base64.urlsafe_b64encode(b'{"sub":"123","name":"John"}').decode().rstrip("=")
        secret = "secret"

        signature = hmac.new(secret.encode(), f"{header}.{payload}".encode(), hashlib.sha256).digest()
        jwt = f"{header}.{payload}.{base64.urlsafe_b64encode(signature).decode().rstrip('=')}"

        self.assertTrue(verify_hs256(jwt, secret))
        self.assertFalse(verify_hs256(jwt, "wrongsecret"))

    def test_verify_rs256(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

        header = base64.urlsafe_b64encode(b'{"alg":"RS256","typ":"JWT"}').decode().rstrip("=")
        payload = base64.urlsafe_b64encode(b'{"sub":"123","name":"John"}').decode().rstrip("=")
        message = f"{header}.{payload}".encode()
        signature = private_key.sign(
            message,
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        jwt = f"{header}.{payload}.{base64.urlsafe_b64encode(signature).decode().rstrip('=')}"

        self.assertTrue(verify_rs256(jwt, public_pem))

        wrong_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        wrong_public_pem = wrong_private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()
        self.assertFalse(verify_rs256(jwt, wrong_public_pem))

    def test_verify_ps256(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

        header = base64.urlsafe_b64encode(b'{"alg":"PS256","typ":"JWT"}').decode().rstrip("=")
        payload = base64.urlsafe_b64encode(b'{"sub":"123","name":"John"}').decode().rstrip("=")
        message = f"{header}.{payload}".encode()
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        jwt = f"{header}.{payload}.{base64.urlsafe_b64encode(signature).decode().rstrip('=')}"

        self.assertTrue(verify_ps256(jwt, public_pem))

        wrong_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        wrong_public_pem = wrong_private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()
        self.assertFalse(verify_ps256(jwt, wrong_public_pem))

    def test_verify_ecdsa(self):
        private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        public_key = private_key.public_key()

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

        header = base64.urlsafe_b64encode(b'{"alg":"ES256","typ":"JWT"}').decode().rstrip("=")
        payload = base64.urlsafe_b64encode(b'{"sub":"123","name":"John"}').decode().rstrip("=")
        message = f"{header}.{payload}".encode()
        signature = private_key.sign(
            message,
            ec.ECDSA(hashes.SHA256()),
        )
        jwt = f"{header}.{payload}.{base64.urlsafe_b64encode(signature).decode().rstrip('=')}"

        self.assertTrue(verify_ecdsa(jwt, public_pem))

        wrong_private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        wrong_public_pem = wrong_private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()
        self.assertFalse(verify_ecdsa(jwt, wrong_public_pem))

    # AES DECRYPTION TESTS
    def test_aes_cbc_decrypt(self):
        key = b"\x00" * 32
        iv = b"\x01" * 16
        data = b"Hello, AES!"
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

        encryptor = cipher.encryptor()
        padder = PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        decrypted = aes_cbc_decrypt(key, iv, encrypted)
        self.assertEqual(decrypted, data.decode('utf-8'))

    def test_aes_gcm_decrypt(self):
        key = b"\x00" * 32
        iv = b"\x01" * 12
        data = b"Hello, AES-GCM!"
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())

        encryptor = cipher.encryptor()
        encryptor.authenticate_additional_data(b"")
        encrypted = encryptor.update(data) + encryptor.finalize()
        tag = encryptor.tag

        decrypted = aes_gcm_decrypt(key, iv, encrypted, tag)
        self.assertEqual(decrypted, data.decode('utf-8'))

if __name__ == "__main__":
    unittest.main()
