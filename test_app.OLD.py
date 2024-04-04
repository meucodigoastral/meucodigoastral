import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    # Garante que a página inicial carrega corretamente
    def test_index_loads(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Garante que a página de cálculo retorna uma resposta para entrada válida
    def test_calculo_valido(self):
        tester = app.test_client(self)
        response = tester.post('/calcular', data=dict(nome="Teste"), follow_redirects=True)
        self.assertIn(b'Resultado da Numerologia', response.data)

    # Garante que a página de cálculo trata entradas inválidas
    def test_calculo_invalido(self):
        tester = app.test_client(self)
        response = tester.post('/calcular', data=dict(nome="123"), follow_redirects=True)
        self.assertIn(b'O nome não deve conter números.', response.data)

if __name__ == '__main__':
    unittest.main()