import os
import unittest
import axado


class TestAxadoArguments(unittest.TestCase):
    def setUp(self):
        self.args = ['axado.py','florianopolis','brasilia','50','7']

    def test_arguments_length(self):
        self.assertEqual(len(axado.extract_and_validate_args(self.args)), 4)

    def test_arguments_type(self):
        origem, destino, nota_fiscal, peso = axado.extract_and_validate_args(self.args)
        self.assertIsInstance(origem, str)
        self.assertIsInstance(destino, str)
        self.assertIsInstance(nota_fiscal, int)
        self.assertIsInstance(peso, int)

    def test_arguments_value(self):
        origem, destino, nota_fiscal, peso = axado.extract_and_validate_args(self.args)
        self.assertEqual(origem, 'florianopolis')
        self.assertEqual(destino, 'brasilia')
        self.assertEqual(nota_fiscal, 50)
        self.assertEqual(peso, 7)


class TestAxadoParseRoutesTableOne(unittest.TestCase):
    def setUp(self):
        args = ['axado.py','florianopolis','brasilia','50','7']
        self.origem, self.destino, self.nota_fiscal, self.peso = axado.extract_and_validate_args(args)
        self.rotas_path = os.path.join('tabela','rotas.csv')

    def teste_parse_rotas_length(self):
        self.assertEqual(
            len(axado.parse_rota_csv(self.origem, self.destino, self.rotas_path)),
            6
        )

    def teste_parse_rotas_type(self):
        origem, destino, prazo, seguro, kg, fixa = axado.parse_rota_csv(self.origem, self.destino, self.rotas_path)
        self.assertIsInstance(origem, str)
        self.assertIsInstance(destino, str)
        self.assertIsInstance(prazo, int)
        self.assertIsInstance(seguro, int)
        self.assertIsInstance(kg, str)
        self.assertIsInstance(fixa, int)

    def teste_parse_rotas_value(self):
        origem, destino, prazo, seguro, kg, fixa = axado.parse_rota_csv(self.origem, self.destino, self.rotas_path)
        self.assertEqual(origem, 'florianopolis')
        self.assertEqual(destino, 'brasilia')
        self.assertEqual(prazo, 3)
        self.assertEqual(seguro, 3)
        self.assertEqual(kg, 'flo')
        self.assertEqual(fixa, 13)


if __name__ == '__main__':
    unittest.main()


