import unittest
import time
from datetime import datetime, timedelta
from src.backend import dummy_data

class TestDummyData(unittest.TestCase):
    def setUp(self):
        """Reset data before each test."""
        dummy_data.bpm_data.clear()
        dummy_data.spo2_data.clear()
        dummy_data.time_data.clear()
        dummy_data.ecg_data.clear()
        dummy_data.last_get_times = {'bpm': None, 'spo2': None, 'time': None, 'ecg': None}

    def test_initial_state(self):
        """Test initial data lists are empty and time since last is None."""
        self.assertIsNone(dummy_data.get_time_since_last('bpm'))
        self.assertIsNone(dummy_data.get_time_since_last('spo2'))
        self.assertIsNone(dummy_data.get_time_since_last('time'))
        self.assertIsNone(dummy_data.get_time_since_last('ecg'))
        self.assertEqual(dummy_data.get_bpm(), [])
        self.assertEqual(dummy_data.get_spo2(), [])
        self.assertEqual(dummy_data.get_time(), [])
        self.assertEqual(dummy_data.get_ecg(), [])

    def test_generate_one_data_point(self):
        """Test generating a single data point increases list lengths."""
        result = dummy_data.fake_data_generator()
        self.assertEqual(len(dummy_data.bpm_data), 1)
        self.assertEqual(len(dummy_data.spo2_data), 1)
        self.assertEqual(len(dummy_data.time_data), 1)
        self.assertEqual(len(dummy_data.ecg_data), 1)
        bpm = dummy_data.bpm_data[0]
        spo2 = dummy_data.spo2_data[0]
        timestamp = dummy_data.time_data[0]
        ecg = dummy_data.ecg_data[0]
        self.assertIsInstance(bpm, (int, float))
        self.assertTrue(60 <= bpm <= 100)
        self.assertIsInstance(spo2, int)
        self.assertTrue(95 <= spo2 <= 100)
        self.assertIsInstance(timestamp, datetime)
        self.assertIsInstance(ecg, list)
        self.assertEqual(len(ecg), 100)
        self.assertTrue(all(isinstance(p, float) for p in ecg))
        self.assertEqual(result['bpm_data'], dummy_data.bpm_data)
        self.assertEqual(result['spo2_data'], dummy_data.spo2_data)
        self.assertEqual(result['time_data'], dummy_data.time_data)
        self.assertEqual(result['ecg_data'], dummy_data.ecg_data)

    def test_generate_multiple_data_points(self):
        """Test generating multiple data points."""
        num_points = 3
        for _ in range(num_points):
            dummy_data.fake_data_generator()
        self.assertEqual(len(dummy_data.bpm_data), num_points)
        self.assertEqual(len(dummy_data.spo2_data), num_points)
        self.assertEqual(len(dummy_data.time_data), num_points)
        self.assertEqual(len(dummy_data.ecg_data), num_points)
        for bpm in dummy_data.bpm_data:
            self.assertTrue(60 <= bpm <= 100)
        for ecg_list in dummy_data.ecg_data:
            self.assertEqual(len(ecg_list), 100)

    def test_get_functions_return_data(self):
        """Test get functions return the generated data lists."""
        dummy_data.fake_data_generator()
        self.assertEqual(dummy_data.get_bpm(), dummy_data.bpm_data)
        self.assertEqual(dummy_data.get_spo2(), dummy_data.spo2_data)
        self.assertEqual(dummy_data.get_time(), dummy_data.time_data)
        self.assertEqual(dummy_data.get_ecg(), dummy_data.ecg_data)
        self.assertEqual(len(dummy_data.get_bpm()), 1)
        self.assertEqual(len(dummy_data.get_ecg()), 1)

    def test_time_since_last_tracking(self):
        """Test that time tracking updates after get calls."""
        self.assertIsNone(dummy_data.get_time_since_last('bpm'))
        self.assertIsNone(dummy_data.get_time_since_last('spo2'))
        self.assertIsNone(dummy_data.get_time_since_last('time'))
        self.assertIsNone(dummy_data.get_time_since_last('ecg'))
        dummy_data.get_bpm()
        self.assertIsInstance(dummy_data.get_time_since_last('bpm'), timedelta)
        dummy_data.get_spo2()
        self.assertIsInstance(dummy_data.get_time_since_last('spo2'), timedelta)
        dummy_data.get_time()
        self.assertIsInstance(dummy_data.get_time_since_last('time'), timedelta)
        dummy_data.get_ecg()
        self.assertIsInstance(dummy_data.get_time_since_last('ecg'), timedelta)

if __name__ == '__main__':
    unittest.main()