import unittest
import sys
sys.path.insert(0, '.')
from app import create_app, create_db, app, db
from unittest.mock import patch, MagicMock, Mock
from src.services.auth_services import flow
import json

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

class TestCallbackEndpoint(BaseTestCase):
    @patch('src.services.auth_services.User')
    @patch('src.services.auth_services.flow')
    @patch('src.services.auth_services.id_token.verify_oauth2_token')
    def test_callback_success(self, mock_verify_oauth,mock_flow,mock_user):
        
        # Simula el valor de 'state' en los argumentos de la solicitud
        with self.client.session_transaction() as session:
            session['state'] = 'random_state_value'
        # Configura el mock de fetch_token para que no haga nada, ya que no necesitas una respuesta
        mock_credentials = Mock()
        mock_credentials.access_token = 'valid_access_token'
        mock_flow.return_value = mock_credentials

        # Configura el mock de verify_oauth2_token para devolver información de usuario simulada
        mock_verify_oauth.return_value = {
            "sub": "8888888",
            "name": "Nicolas Hurtado",
            "picture": "https://fastly.picsum.photos/id/600/200/300.jpg?hmac=Ub3Deb_eQNe0Un7OyE33D79dnextn3M179L0nRkv1eg"
            # Agrega más datos según sea necesario
        }
        # Configura la base de datos SQLite en memoria
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        # Crea todas las tablas en la base de datos
        create_db()
        mock_user.query.filter_by.first.return_value = None
        # Configura el mock de User
        response = self.client.get('/callback?state=random_state_value')

        # Verifica que la solicitud sea redirigida a /protected_area
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/protected_area')
        
        # Verifica que los datos del usuario estén almacenados en la sesión
        with self.client.session_transaction() as session:
            self.assertEqual(session['google_id'], '8888888')
            self.assertEqual(session['name'], 'Nicolas Hurtado')
            self.assertEqual(session['img'], 'https://fastly.picsum.photos/id/600/200/300.jpg?hmac=Ub3Deb_eQNe0Un7OyE33D79dnextn3M179L0nRkv1eg')

        
        
if __name__ == '__main__':
    unittest.main()
