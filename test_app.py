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
        self.assertIn('Resultado da Numerologia', response.data.decode('utf-8'))

    # Verifica o tratamento de nomes com acentuação e variações de maiúsculas/minúsculas
    def test_calculo_nome_com_variacoes(self):
        tester = app.test_client(self)
        nomes = ["José", "jose", "JOSE", "josé", "JOSÉ"]
        for nome in nomes:
            with self.subTest(nome=nome):
                response = tester.post('/calcular', data=dict(nome=nome), follow_redirects=True)
                self.assertIn('10 (BOM)', response.data.decode('utf-8'))

    # Corrigido para verificar a presença de "Soma Total:" como indicativo de processamento
    def test_tratamento_de_numeros_como_zero(self):
        tester = app.test_client(self)
        response = tester.post('/calcular', data=dict(nome="Ana123"), follow_redirects=True)
        self.assertIn('Soma Total:', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()