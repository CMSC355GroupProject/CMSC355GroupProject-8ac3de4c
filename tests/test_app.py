#Imports
import unittest
from unittest.mock import patch
import os
import sys
from flask import Flask

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/backend')))

from app import create_app

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #Initialize test vars
        os.environ['SECRET_KEY'] = 'test-secret-key'
        os.environ['MONGO_URI'] = 'mongodb://localhost:27017/testdb'

    def setUp(self):
        #Initialize test client
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        #Clean up
        self.app_context.pop()

    def test_app(self):
        #Verify app
        self.assertIsInstance(self.app, Flask)
        for key in ['MONGO_URI', 'JWT_SECRET_KEY', 'SECRET_KEY']:
            self.assertIsNotNone(self.app.config[key])

    @patch('app.render_template')
    def test_routes(self, mock_render):
        #Test routes
        for route, template in [('/', 'login.html'),
                              ('/register', 'register.html'),
                              ('/index', 'index.html'),
                              ('/alerts', 'alerts.html')]:
            mock_render.return_value = f"Mocked {template}"
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200)
            mock_render.assert_called_once_with(template)
            mock_render.reset_mock()