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
        self.assertIsInstance(nota_fiscal, float)
        self.assertIsInstance(peso, float)

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
            len(axado.parse_route_file_csv(self.origem, self.destino, self.rotas_path)),
            6
        )

    def teste_parse_rotas_type(self):
        origem, destino, prazo, seguro, kg, fixa = axado.parse_route_file_csv(self.origem, self.destino, self.rotas_path)
        self.assertIsInstance(origem, str)
        self.assertIsInstance(destino, str)
        self.assertIsInstance(prazo, int)
        self.assertIsInstance(seguro, int)
        self.assertIsInstance(kg, str)
        self.assertIsInstance(fixa, int)

    def teste_parse_rotas_value(self):
        origem, destino, prazo, seguro, kg, fixa = axado.parse_route_file_csv(self.origem, self.destino, self.rotas_path)
        self.assertEqual(origem, 'florianopolis')
        self.assertEqual(destino, 'brasilia')
        self.assertEqual(prazo, 3)
        self.assertEqual(seguro, 3)
        self.assertEqual(kg, 'flo')
        self.assertEqual(fixa, 13)


class TestAxadoCalculus(unittest.TestCase):
    def setUp(self):
        self.seguro_um = 3
        self.seguro_dois = 2
        self.nota_fiscal = 50.0
        self.fixa = 13
        self.peso = 7.0
        self.preco_um = 12.0
        self.preco_dois = 14.5
        self.alfandega = 0
        self.taxa_icms = 6.0
        self.tabela_um = 104.79
        self.tabela_dois = 109.05

    def test_calculus_table_one(self):
        self.assertEqual(
            axado.calculate_table_one(self.seguro_um, self.nota_fiscal, self.fixa,
                                      self.peso, self.preco_um, self.taxa_icms),
            self.tabela_um
        )

    def test_calculus_table_two(self):
        self.assertEqual(
            axado.calculate_table_two(self.seguro_dois, self.nota_fiscal, self.peso,
                                      self.preco_dois, self.alfandega, self.taxa_icms),
            self.tabela_dois
        )


if __name__ == '__main__':
    unittest.main()


