import unittest
import subprocess
import os

class TestSecrets(unittest.TestCase):

    def test_length(self):
        """Test secret key length"""
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src/backend/generate_secrets.py')
        
        #Use subprocess to avoid running on import.
        res = subprocess.run(
            ['python', path],
            capture_output=True,
            text=True,
            check=True
        )
        #Test output
        out = res.stdout.strip()
        self.assertEqual(len(out), 64, "Expected 64 chars.")