import base64
import hashlib
import zlib
import gzip
import codecs
import binascii

# Define decoding functions
def decode_base64(data):
    try:
        return base64.urlsafe_b64decode(data + '===').decode('utf-8')
    except Exception:
        return None

def decode_base58(data):
    try:
        alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        base_count = len(alphabet)
        decoded = 0
        for char in data:
            decoded = decoded * base_count + alphabet.index(char)

        # Convert the integer to bytes
        byte_array = []
        while decoded > 0:
            byte_array.append(decoded % 256)
            decoded //= 256
        byte_array.reverse()

        # Decode bytes to UTF-8 and capitalize for correct format
        return bytes(byte_array).decode("utf-8").capitalize()
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

def hash_md5(data):
    try:
        return hashlib.md5(data.encode()).hexdigest()
    except Exception:
        return None

def hash_sha256(data):
    try:
        return hashlib.sha256(data.encode()).hexdigest()
    except Exception:
        return None

def hash_sha1(data):
    try:
        return hashlib.sha1(data.encode()).hexdigest()
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

def decode_ascii85(data):
    try:
        # Remove the `<~` and `~>` delimiters for decoding
        if data.startswith("<~") and data.endswith("~>"):
            data = data[2:-2]
        decoded = base64.a85decode(data).decode("utf-8")
        return decoded
    except Exception as e:
        print(f"Ascii85 decoding error: {e}")
        return None

def decode_base32(data):
    try:
        return base64.b32decode(data).decode('utf-8')
    except Exception:
        return None

def decode_base16(data):
    try:
        return base64.b16decode(data).decode('utf-8')
    except Exception:
        return None

def decode_unicode_escape(data):
    try:
        return data.encode().decode('unicode_escape')
    except Exception:
        return None

# Decoding operation mapping
operations = {
    "Base64": decode_base64,
    "Base58": decode_base58,
    "ROT13": decode_rot13,
    "Gzip": decompress_gzip,
    "Zlib": decompress_zlib,
    "MD5 Hash": hash_md5,
    "SHA-256 Hash": hash_sha256,
    "SHA-1 Hash": hash_sha1,
    "Hexadecimal": decode_hex,
    "Binary": decode_binary,
    "URL Encoding": decode_url,
    "Ascii85": decode_ascii85,
    "Base32": decode_base32,
    "Base16": decode_base16,
    "Unicode Escape": decode_unicode_escape,
}
