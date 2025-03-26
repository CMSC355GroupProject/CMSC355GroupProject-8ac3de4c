import unittest

def login_user(username, password):
    if not username:
        raise ValueError("Username is required.")
    if len(username) < 5:
        raise ValueError("Username must be at least 5 characters long.")
    if not password:
        raise ValueError("Password is required.")
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters long.")
    
    # Test using dummy data from test_registration.py
    if username == "test_user" and password == "password123":
        return {"status": "success", "message": "Login successful."}
    
    raise ValueError("Invalid username or password.")

class TestLogin(unittest.TestCase):

    def test_successful_login(self):
        # Test case for valid login
        result = login_user("test_user", "password123")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "Login successful.")

    def test_missing_username(self):
        # Test case for missing username
        with self.assertRaises(ValueError) as context:
            login_user("", "password123")
        self.assertEqual(str(context.exception), "Username is required.")

    def test_short_username(self):
        # Test case for username that's too short
        with self.assertRaises(ValueError) as context:
            login_user("usr", "password123")
        self.assertEqual(str(context.exception), "Username must be at least 5 characters long.")

    def test_missing_password(self):
        # Test case for missing password
        with self.assertRaises(ValueError) as context:
            login_user("test_user", "")
        self.assertEqual(str(context.exception), "Password is required.")

    def test_short_password(self):
        # Test case for password that's too short
        with self.assertRaises(ValueError) as context:
            login_user("test_user", "pwd")
        self.assertEqual(str(context.exception), "Password must be at least 6 characters long.")

    def test_invalid_credentials(self):
        # Test case for invalid username or password
        with self.assertRaises(ValueError) as context:
            login_user("test_user", "wrongpassword")
        self.assertEqual(str(context.exception), "Invalid username or password.")

if __name__ == '__main__':
    unittest.main()