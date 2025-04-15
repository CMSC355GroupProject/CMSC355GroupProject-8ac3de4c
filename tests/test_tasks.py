#Imports
import unittest
from unittest.mock import patch, MagicMock, call
from datetime import datetime
from bson import ObjectId
import os
import sys

#Import tasks
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/backend')))
from tasks import generate_loop, client as tasks_client

class TestTasks(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        #Close MongoDB
        tasks_client.close()

    @patch('tasks.db')
    @patch('tasks.time.sleep', side_effect=KeyboardInterrupt)
    @patch('tasks.generate_vital_data')
    def test_generate_loop(self, test_generate_vital, test_sleep, test_db):
        """Test loop function."""
        test_patient = {"_id": ObjectId(), "name": "Test"}
        test_db.patients.find.return_value = [test_patient]
        test_generate_vital.return_value = {"patient_id": test_patient["_id"], "heart_rate": 80}

        with self.assertRaises(KeyboardInterrupt):
            generate_loop()

        test_db.patients.find.assert_called_once()
        test_generate_vital.assert_called_once_with(test_patient["_id"])
        
        inserted_doc = test_db.vitals.insert_one.call_args[0][0]
        self.assertEqual(inserted_doc["patient_id"], test_patient["_id"])
        self.assertIsInstance(inserted_doc["timestamp"], datetime)
        
        test_sleep.assert_called_once_with(5)