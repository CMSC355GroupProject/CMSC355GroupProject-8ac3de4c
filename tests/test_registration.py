import unittest
from datetime import datetime

def register_user(username, email, password, dob, height, weight, biological_gender, phone_number):
    # Validate username
    if not username:
        raise ValueError("Username is required.")
    if len(username) < 5:
        raise ValueError("Username must be at least 5 characters long.")
    # Validate email
    if '@' not in email or '.' not in email:
        raise ValueError("Invalid email address.")
    # Validate password - boundary value analysis
    if not password:
        raise ValueError("Password is required.")
    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters long.")
    # Validate date of birth
    try:
        dob_date = datetime.strptime(dob, "%m-%d-%Y")
        current_date = datetime.now()
        if dob_date > current_date:
            raise ValueError("Date of birth cannot be in the future.")
    except ValueError:
        raise ValueError("Invalid date of birth format. Use MM-DD-YYYY.")
    # Validate height with feet and inches
    if height is None:
        raise ValueError("Height is required.")
    if not isinstance(height, str):
        raise ValueError("Height must be in format 'X'Y\"' where X is feet and Y is inches.")
    try:
        # Parse height string (e.g., "5'11"")
        feet, inches = height.split("'")
        inches = inches.rstrip('"')
        feet = int(feet)
        inches = int(inches)
        
        if feet < 0 or inches < 0:
            raise ValueError("Height values cannot be negative.")
        if feet > 8:  # Reasonable upper boundary in feet
            raise ValueError("Height value is unreasonably high.")
        if inches >= 12:
            raise ValueError("Inches must be less than 12.")
    except (ValueError, IndexError):
        raise ValueError("Height must be in format 'X'Y\"' where X is feet and Y is inches.")
    # Validate weight with boundary values
    if weight is None:
        raise ValueError("Weight is required.")
    if not isinstance(weight, (int, float)):
        raise ValueError("Weight must be a number.")
    if weight <= 0:
        raise ValueError("Weight must be a positive number.")
    if weight > 500:  
        raise ValueError("Weight value is unreasonably high.")
    # Validate biological gender
    if not biological_gender:
        raise ValueError("Biological gender is required.")
    if biological_gender not in ['male', 'female']:
        raise ValueError("Biological gender must be 'male' or 'female'")
    # Validate phone number
    if not phone_number:
        raise ValueError("Phone number is required.")
    if len(phone_number) != 10 or not phone_number.isdigit():
        raise ValueError("Phone number must be a 10-digit number.")
    
    return {"status": "success", "message": "Registration successful."}


class TestRegistration(unittest.TestCase):

    def test_successful_registration(self):
        # Test case for valid registration
        result = register_user(
            "test_user", "test_user@testing.com", "password123", "05-15-1990", "5'11\"", 75, "male", "1234567890"
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message"], "Registration successful.")

    def test_missing_username(self):
        # Test case for missing username
        with self.assertRaises(ValueError) as context:
            register_user("", "test_user@testing.com", "password123", "05-15-1990", "5'11\"", 75, "male", "1234567890")
        self.assertEqual(str(context.exception), "Username is required.")

    def test_invalid_email(self):
        # Test case for invalid email
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user.com", "password123", "05-15-1990", "5'11\"", 75, "male", "1234567890")
        self.assertEqual(str(context.exception), "Invalid email address.")

    def test_short_password(self):
        # Test case for password that's too short
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user@testing.com", "pwd", "05-15-1990", "5'11\"", 75, "male", "1234567890")
        self.assertEqual(str(context.exception), "Password must be at least 6 characters long.")

    def test_invalid_dob_format(self):
        # Test case for invalid date of birth format
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user@testing.com", "password123", "1990-15-05", "5'11\"", 75, "male", "1234567890")
        self.assertEqual(str(context.exception), "Invalid date of birth format. Use MM-DD-YYYY.")

    def test_invalid_height(self):
        # Test case for invalid height format
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user@testing.com", "password123", "05-15-1990", "invalid", 75, "male", "1234567890")
        self.assertEqual(str(context.exception), "Height must be in format 'X'Y\"' where X is feet and Y is inches.")

    def test_invalid_weight(self):
        # Test case for invalid weight (negative or zero)
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user@testing.com", "password123", "05-15-1990", "5'11\"", -75, "male", "1234567890")
        self.assertEqual(str(context.exception), "Weight must be a positive number.")

    def test_invalid_biological_gender(self):
        # Test case for invalid biological gender
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user@testing.com", "password123", "05-15-1990", "5'11\"", 75, "unknown", "1234567890")
        self.assertEqual(str(context.exception), "Biological gender must be 'male' or 'female'")

    def test_invalid_phone_number(self):
        # Test case for invalid phone number
        with self.assertRaises(ValueError) as context:
            register_user("test_user", "test_user@testing.com", "password123", "05-15-1990", "5'11\"", 75, "male", "12345")
        self.assertEqual(str(context.exception), "Phone number must be a 10-digit number.")

if __name__ == '__main__':
    unittest.main()