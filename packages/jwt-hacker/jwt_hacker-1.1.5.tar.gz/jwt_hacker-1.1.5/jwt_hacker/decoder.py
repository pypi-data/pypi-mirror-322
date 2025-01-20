import base64
import hashlib
import hmac
import zlib
import gzip
import codecs
import binascii
import json
import requests
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding, ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
# from cryptography.hazmat.primitives.kdf.argon2 import Argon2
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization



# BASE DECODING FUNCTIONS
def decode_base64(data):
    try:
        return base64.urlsafe_b64decode(data + '===').decode('utf-8')
    except Exception:
        return None

def decode_base32(data):
    try:
        return base64.b32decode(data).decode('utf-8')
    except Exception:
        return None

def decode_base58(data):
    try:
        alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        base_count = len(alphabet)
        decoded = 0
        for char in data:
            decoded = decoded * base_count + alphabet.index(char)

        byte_array = []
        while decoded > 0:
            byte_array.append(decoded % 256)
            decoded //= 256
        byte_array.reverse()
        return bytes(byte_array).decode("utf-8").capitalize()
    except Exception:
        return None

def decode_ascii85(data):
    try:
        if data.startswith("<~") and data.endswith("~>"):
            data = data[2:-2]
        return base64.a85decode(data).decode("utf-8")
    except Exception:
        return None

def decode_hex(data):
    try:
        return bytes.fromhex(data).decode('utf-8')
    except Exception:
        return None

def decode_binary(data):
    try:
        return ''.join(chr(int(data[i:i+8], 2)) for i in range(0, len(data), 8))
    except Exception:
        return None

def decode_url(data):
    try:
        from urllib.parse import unquote
        return unquote(data)
    except Exception:
        return None

def decode_rot13(data):
    try:
        return codecs.decode(data, 'rot_13')
    except Exception:
        return None

def decompress_gzip(data):
    try:
        return gzip.decompress(base64.b64decode(data)).decode('utf-8')
    except Exception:
        return None

def decompress_zlib(data):
    try:
        return zlib.decompress(base64.b64decode(data)).decode('utf-8')
    except Exception:
        return None

# HASHING FUNCTIONS
def hash_md5(data):
    try:
        return hashlib.md5(data.encode()).hexdigest()
    except Exception:
        return None

def hash_sha1(data):
    try:
        return hashlib.sha1(data.encode()).hexdigest()
    except Exception:
        return None

def hash_sha256(data):
    try:
        return hashlib.sha256(data.encode()).hexdigest()
    except Exception:
        return None

def hash_sha512(data):
    try:
        return hashlib.sha512(data.encode()).hexdigest()
    except Exception:
        return None

def hash_sha3_256(data):
    try:
        return hashlib.sha3_256(data.encode()).hexdigest()
    except Exception:
        return None

def hash_sha3_512(data):
    try:
        return hashlib.sha3_512(data.encode()).hexdigest()
    except Exception:
        return None

# JWT VERIFICATION FUNCTIONS
def verify_hs256(jwt, secret):
    try:
        header, payload, signature = jwt.split('.')
        signature_check = hmac.new(
            key=secret.encode(),
            msg=f"{header}.{payload}".encode(),
            digestmod=hashlib.sha256
        ).digest()
        expected_signature = base64.urlsafe_b64encode(signature_check).rstrip(b'=').decode()
        return signature == expected_signature
    except Exception:
        return False

def verify_rs256(jwt, public_key_pem):
    try:
        header, payload, signature = jwt.split('.')
        decoded_signature = base64.urlsafe_b64decode(signature + '===')
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        public_key.verify(
            decoded_signature,
            f"{header}.{payload}".encode(),
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True
    except Exception as e:
        print(f"RS256 verification error: {e}")
        return False

def verify_ps256(jwt, public_key_pem):
    try:
        header, payload, signature = jwt.split('.')
        decoded_signature = base64.urlsafe_b64decode(signature + '===')
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        public_key.verify(
            decoded_signature,
            f"{header}.{payload}".encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        return True
    except Exception as e:
        print(f"PS256 verification error: {e}")
        return False

def verify_ecdsa(jwt, public_key_pem):
    try:
        header, payload, signature = jwt.split('.')
        decoded_signature = base64.urlsafe_b64decode(signature + '===')
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        public_key.verify(
            decoded_signature,
            f"{header}.{payload}".encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except Exception as e:
        print(f"ECDSA verification error: {e}")
        return False

# AES DECRYPTION
def aes_cbc_decrypt(key, iv, ciphertext):
    try:
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
        return decrypted.decode('utf-8')
    except Exception:
        return None

def aes_gcm_decrypt(key, iv, ciphertext, tag):
    try:
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted.decode('utf-8')
    except Exception:
        return None

# JWE DECRYPTION
def decrypt_jwe(jwe_token, private_key_pem):
    try:
        header, encrypted_key, iv, ciphertext, tag = jwe_token.split('.')
        private_key = serialization.load_pem_private_key(private_key_pem.encode(), password=None)
        
        decrypted_key = private_key.decrypt(
            base64.urlsafe_b64decode(encrypted_key + '==='),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )

        iv = base64.urlsafe_b64decode(iv + '===')
        ciphertext = base64.urlsafe_b64decode(ciphertext + '===')
        tag = base64.urlsafe_b64decode(tag + '===')

        return aes_gcm_decrypt(decrypted_key, iv, ciphertext, tag)
    except Exception as e:
        print(f"JWE decryption error: {e}")
        return None

# CLAIM VALIDATION
def validate_claims(payload):
    try:
        claims = json.loads(base64.urlsafe_b64decode(payload + '===').decode('utf-8'))
        now = datetime.now(timezone.utc).timestamp()

        if 'exp' in claims and now > claims['exp']:
            return "Token expired."
        if 'nbf' in claims and now < claims['nbf']:
            return "Token not yet valid."
        if 'iat' in claims and now < claims['iat']:
            return "Token issued in the future."

        return "Claims valid."
    except Exception as e:
        return f"Claim validation error: {e}"

# JWK/JWKS SUPPORT
def parse_jwk(jwk):
    try:
        return serialization.load_pem_public_key(jwk.encode())
    except Exception as e:
        print(f"JWK parsing error: {e}")
        return None

def get_key_from_jwks(jwks_url, kid):
    try:
        response = requests.get(jwks_url)
        keys = response.json().get('keys', [])
        for key in keys:
            if key.get('kid') == kid:
                return parse_jwk(key)
        return None
    except Exception as e:
        print(f"JWKS retrieval error: {e}")
        return None

# KEY DERIVATION
def derive_key_pbkdf2(password, salt, iterations=100000, length=32):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=length, salt=salt, iterations=iterations)
    return kdf.derive(password.encode())

def derive_key_scrypt(password, salt, length=32):
    kdf = Scrypt(salt=salt, length=length, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())

def derive_key_argon2(password, salt, length=32):
    kdf = Argon2(type=Argon2.Type.ID, memory_cost=65536, time_cost=3, parallelism=4)
    return kdf.derive(password.encode())

# Decoding operation mapping
operations = {
    "Base64": decode_base64,
    "Base32": decode_base32,
    "Base58": decode_base58,
    "Ascii85": decode_ascii85,
    "Hexadecimal": decode_hex,
    "Binary": decode_binary,
    "URL Encoding": decode_url,
    "ROT13": decode_rot13,
    "Gzip": decompress_gzip,
    "Zlib": decompress_zlib,
    "MD5 Hash": hash_md5,
    "SHA-1 Hash": hash_sha1,
    "SHA-256 Hash": hash_sha256,
    "SHA-512 Hash": hash_sha512,
    "SHA3-256 Hash": hash_sha3_256,
    "SHA3-512 Hash": hash_sha3_512,
    "HS256 Verify": verify_hs256,
    "RS256 Verify": verify_rs256,
    "PS256 Verify": verify_ps256,
    "ECDSA Verify": verify_ecdsa,
    "AES-CBC Decrypt": aes_cbc_decrypt,
    "AES-GCM Decrypt": aes_gcm_decrypt,
    "Validate Claims": validate_claims,
    "JWE Decrypt": decrypt_jwe,
    "PBKDF2 Key Derivation": derive_key_pbkdf2,
    "Scrypt Key Derivation": derive_key_scrypt,
    "Argon2 Key Derivation": derive_key_argon2
}
