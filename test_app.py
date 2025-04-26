import unittest
from app import validar_preco, validar_data, validar_id

class TesteProduto(unittest.TestCase):

    def test_validar_preco_positivo(self):
        self.assertEqual(validar_preco("10.5"), 10.5)

    def test_validar_preco_invalido(self):
        self.assertIsNone(validar_preco("-5"))
        self.assertIsNone(validar_preco("abc"))

    def test_validar_data_valida(self):
        self.assertTrue(validar_data("2099-12-31"))

    def test_validar_data_invalida(self):
        self.assertFalse(validar_data("2022/12/31"))
        self.assertFalse(validar_data("2022-15-31"))

    def test_validar_id_valido(self):
        self.assertEqual(validar_id("5"), 5)

    def test_validar_id_invalido(self):
        self.assertIsNone(validar_id("0"))
        self.assertIsNone(validar_id("-1"))
        self.assertIsNone(validar_id("abc"))

if __name__ == '__main__':
    unittest.main()
