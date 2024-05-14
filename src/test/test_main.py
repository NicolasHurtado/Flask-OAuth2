import unittest
import os
import pytest
import sys
sys.path.insert(0, '.')
from app import create_app

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            # Realiza inicializaciones necesarias, como crear la base de datos
            pass

    def tearDown(self):
        with self.app.app_context():
            # Realiza limpieza necesaria, como eliminar la base de datos
            pass

class TestMainServices(BaseTestCase):
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_protected_area_page_without_login(self):
        response = self.client.get('/protected_area')
        self.assertEqual(response.status_code, 401)

    # Agrega más pruebas según sea necesario

if __name__ == '__main__':
    unittest.main()
