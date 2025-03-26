import unittest
from datetime import datetime

def register_user(username, email, password, dob, height, weight, biological_gender, phone_number):
    if not username:
        raise ValueError("Username is required.")
    if len(username) < 5:
        raise ValueError("Username must be at least 5 characters long.")
    if '@' not in email:
        raise ValueError("Invalid email address.")
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters long.")
    try:
        datetime.strptime(dob, "%m-%d-%Y")
    except ValueError:
        raise ValueError("Invalid date of birth format. Use MM-DD-YYYY.")
    # Need to decide on a metric for height and boundaries
    if height <= 0:
        raise ValueError("Height must be a positive number.")
    if weight <= 0:
        raise ValueError("Weight must be a positive number.")
    if biological_gender not in ['male', 'female']:
        raise ValueError("Biological gender must be 'male' or 'female'")
    if len(phone_number) != 10 or not phone_number.isdigit():
        raise ValueError("Phone number must be a 10-digit number.")
    
    return {"status": "success", "message": "Registration successful."}


class TestRegistration(unittest.TestCase):

    def test_successful_registration(self):
        # Test case for valid registration
        result = register_user(
            "test_user", "test_user@testing.com", "password123", "05-15-1990", 180, 75, "male", "1234567890"
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "Registration successful.")

    def test_missing_username(self):
        # Test case for missing username
        with self.assertRaises(ValueError) as context:
            register_user("", "test_user@testing.com", "password123", "05-15-1990", 180, 75, "male", "1234567890")
        self.assertEqual(str(context.exception), "Username is required.")

    def test_invalid_email(self):
        # Test case for invalid email
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user.com", "password123", "05-15-1990", 180, 75, "male", "1234567890")
        self.assertEqual(str(context.exception), "Invalid email address.")

    def test_short_password(self):
        # Test case for password that's too short
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user@testing.com", "pwd", "05-15-1990", 180, 75, "male", "1234567890")
        self.assertEqual(str(context.exception), "Password must be at least 6 characters long.")

    def test_invalid_dob_format(self):
        # Test case for invalid date of birth format
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user@testing.com", "password123", "1990-15-05", 180, 75, "male", "1234567890")
        self.assertEqual(str(context.exception), "Invalid date of birth format. Use MM-DD-YYYY.")

    def test_invalid_height(self):
        # Test case for invalid height (negative or zero)
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user@testing.com", "password123", "05-15-1990", -180, 75, "male", "1234567890")
        self.assertEqual(str(context.exception), "Height must be a positive number.")

    def test_invalid_weight(self):
        # Test case for invalid weight (negative or zero)
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user@testing.com", "password123", "05-15-1990", 180, -75, "male", "1234567890")
        self.assertEqual(str(context.exception), "Weight must be a positive number.")

    def test_invalid_biological_gender(self):
        # Test case for invalid biological gender
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user@testing.com", "password123", "05-15-1990", 180, 75, "unknown", "1234567890")
        self.assertEqual(str(context.exception), "Biological gender must be 'male' or 'female'")

    def test_invalid_phone_number(self):
        # Test case for invalid phone number
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user@testing.com", "password123", "05-15-1990", 180, 75, "male", "12345")
        self.assertEqual(str(context.exception), "Phone number must be a 10-digit number.")

if __name__ == '__main__':
    unittest.main()