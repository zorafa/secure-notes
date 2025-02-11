import unittest
from secure_notes import encrypt, decrypt, load_key

class TestSecureNotes(unittest.TestCase):
    def setUp(self):
        self.key = load_key()
        self.message = "Test message"

    def test_encryption_decryption(self):
        encrypted = encrypt(self.message, self.key)
        decrypted = decrypt(encrypted, self.key).decode()
        self.assertEqual(self.message, decrypted)

if __name__ == "__main__":
    unittest.main()
