import unittest
from bson.objectid import ObjectId
from src.backend.models.patient import format_patient

class TestPatient(unittest.TestCase):

    def test_patient(self):
        doc = {
            "_id": ObjectId(),
            "username": "test",
            "email": "test@example.com",
            "dob": "2000-01-01",
            "height": 100,
            "weight": 100,
            "biological_gender": "Male",
            "phone_number": "111-111-1111"
        }
        expected = {
            "id": str(doc["_id"]),
            "username": "test",
            "email": "test@example.com",
            "dob": "2000-01-01",
            "height": 100,
            "weight": 100,
            "biological_gender": "Male",
            "phone_number": "111-111-1111"
        }
        result = format_patient(doc)
        self.assertEqual(result, expected)

    def test_bad_patient(self):
        doc = {
            "_id": ObjectId(),
            "username": "test",
            "email": "test@example.com"
        }
        expected = {
            "id": str(doc["_id"]),
            "username": "test",
            "email": "test@example.com",
            "dob": None,
            "height": None,
            "weight": None,
            "biological_gender": None,
            "phone_number": None
        }
        result = format_patient(doc)
        self.assertEqual(result, expected) 