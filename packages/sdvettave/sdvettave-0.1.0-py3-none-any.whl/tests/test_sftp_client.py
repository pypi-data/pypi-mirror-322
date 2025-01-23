
import unittest
from mytower_etl.extractors.sftp_client import SFTPClient

class TestSFTPClient(unittest.TestCase):
    def test_connect(self):
        sftp = SFTPClient(hostname="test.com", username="user", sftp_private_key="key", port=22)
        self.assertRaises(Exception, sftp.connect)

if __name__ == "__main__":
    unittest.main()
    