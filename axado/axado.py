# -*- coding: utf-8 -*-
"""
    Author: Renato Pacheco Vieira
            renato.pacheco.r2@gmail.com
    Observações:  os comentários, documentação e grande parte do código estão em inglês entretanto algumas variáveis,
                  principalmente aquelas que dizem respeito ao domínio do negócio, se encontram em português devido
                  a dificuldade que trariam para entender os cálculos, ou incompatibilidade/dificuldade de traduzi-las
                  para o inglês.
"""

import sys
import csv
import os


class LimitExceededError(Exception):
    """
        Weight limit exceeded
    """
    pass


class RouteError(Exception):
    """
        Route not found
    """
    pass


class PriceError(Exception):
    """
        Price not found
    """
    pass


def extract_and_validate_args(args):
    """
        Validate arguments provided by user
    :param args: list of all parameter user wrote
    :return: list of parameter cast to right type [<origem>, <destino>, <nota_fiscal>, <peso>]
    """
    if len(args) != 5:
        raise SyntaxError

    try:
        # assuming nota_fiscal represents a price, this value can be float
        nf = float(args[3])
    except:
        raise ValueError('<nota_fiscal> must be a number')

    try:
        # it is not explicit but I assumed peso can be float like in 7.5 kg
        peso = float(args[4])
    except:
        raise ValueError('<peso> must be a number')

    return [args[1], args[2], nf, peso]


def parse_route_file_csv(origin, destination, filename):
    """
        Read route file in csv, look for route (origin, destination) and return information on that line
    :param origin: <origem> inserted by user in args
    :param destination: <destino> inserted by user in args
    :param filename: full file name of route where information is
    :return: information list of that route
    """

    # using 'with' is good in this case to guarantee that file will be closed
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)

        # skip first line, since it is header
        reader.next()

        # iterate over lines of file
        for line in reader:

            # if this route is not the passed in params
            if line[0] != origin or line[1] != destination:

                # pass to next line of file
                continue
            else:
                # this route is the passed in params

                # cast types
                line[2] = int(line[2])
                line[3] = int(line[3])
                line[-1] = int(line[-1])
                return line

    # If no route is found raise an error
    raise RouteError


def parse_price_file_csv(nome, peso, filename, delimiter=','):
    """
        Parse price file in csv, look for <nome> and parse information on that line
    :param nome: parameter found in route file
    :param peso: parameter found in route file
    :param filename: full file name of price where information is
    :param delimiter: in case of tsv files this value must be '\t'
    :return: price for that weight
    """
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        reader.next()
        for line in reader:
            if line[0] != nome:
                continue
            else:
                begin = int(line[1])

                try:
                    end = int(line[2])
                except ValueError:
                    # This case is when that is no value of end.
                    line[-1] = float(line[-1])
                    return line[-1]

                if begin <= peso and peso < end:
                    line[-1] = float(line[-1])
                    return line[-1]
                else:
                    continue

    raise PriceError


def parse_route_tsv(origin, destination, weight, filename):
    """
        Read route file in csv, look for route (origin, destination) and return information on that line
    :param origin: <origem> inserted by user in args
    :param destination: <destino> inserted by user in args
    :param weight: <peso> inserted by user in args
    :param filename: full file name of route where information is
    :return: information list of that route
    """
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        # skip first line, since it is header
        reader.next()

        # iterate over lines of file
        for line in reader:

            # catch weight limit
            limit = int(line[2])

            # if this route is not the passed in params
            if line[0] != origin or line[1] != destination:
                # pass to next line
                continue
            else:
                # this route is the passed in params

                # check if weight, inserted by user, exceed limit
                if limit > 0 and weight > limit:
                    # if yes raise an Error
                    raise LimitExceededError

                # everything is ok than cast information
                info = []
                i = 0
                for i in range(3, 7):
                    info.append(int(line[i]))
                info.append(line[i+1])
                return info

    # If no route is found raise an error
    raise RouteError


def parse_price_tsv(nome, peso, filename):
    """
        Parse price file in tsv, look for <nome> and parse information on that line
    :param nome: parameter found in route file
    :param peso: parameter found in route file
    :param filename: full file name of price where information is
    :return: price for that weight
    """
    return parse_price_file_csv(nome, peso, filename, delimiter='\t')


def calculate_one(origin, destination, nf, weight):
    """
        Prepare information to calculate delivery tax using 'tabela' one, calculate it and print result
    :param origin: <origem> inserted by user in args
    :param destination: <destino> inserted by user in args
    :param nf: <nota_fiscal> inserted by user
    :param weight: <peso> inserted by user in args
    """
    rotas_path = os.path.join('tabela', 'rotas.csv')
    preco_path = os.path.join('tabela', 'preco_por_kg.csv')

    try:
        origem, destino, prazo, seguro, kg, fixa = parse_route_file_csv(origin, destination, rotas_path)
        preco = parse_price_file_csv(kg, weight, preco_path)
    except (RouteError, PriceError):
        print '{0}:{1}, {2}'.format('tabela', '-', '-')
        return

    taxa_icms = 6.0

    total = calculate_table_one(seguro, nf, fixa, weight, preco, taxa_icms)

    print '{0}:{1}, {2}'.format('tabela', prazo, total)


def calculate_table_one(seguro, nota_fiscal, fixa, peso, preco, taxa_icms):
    """
        Calculate total delivery tax using rules of 'tabela'
    """
    seguro = (nota_fiscal * seguro) / 100.0
    faixa = peso * preco
    subtotal = seguro + fixa + faixa

    total = subtotal / ((100.0 - taxa_icms) / 100.0)

    return round(total + .005, 2)


def calculate_two(origin, destination, nf, weight):
    """
        Prepare information to calculate delivery tax using 'tabela2', calculate it and print result
    :param origin: <origem> inserted by user in args
    :param destination: <destino> inserted by user in args
    :param nf: <nota_fiscal> inserted by user
    :param weight: <peso> inserted by user in args
    """
    rotas_path = os.path.join('tabela2', 'rotas.tsv')
    preco_path = os.path.join('tabela2', 'preco_por_kg.tsv')

    try:
        prazo, seguro, taxa_icms, alfandega, kg = parse_route_tsv(origin, destination, weight, rotas_path)
        preco = parse_price_tsv(kg, weight, preco_path)
    except (LimitExceededError, RouteError, PriceError):
        print '{0}:{1}, {2}'.format('tabela2', '-', '-')
        return

    total = calculate_table_two(seguro, nf, weight, preco, alfandega, taxa_icms)

    print '{0}:{1}, {2}'.format('tabela2', prazo, total)


def calculate_table_two(seguro, nota_fiscal, peso, preco, alfandega, taxa_icms):
    """
        Calculate total delivery tax using rules of 'tabela2'
    """
    seguro = nota_fiscal * seguro / 100.0
    faixa = peso * preco
    subtotal = seguro + faixa

    total_alfandega = subtotal * (alfandega / 100.0)
    subtotal += total_alfandega

    total = subtotal / ((100.0 - taxa_icms) / 100.0)
    return round(total + .005, 2)


if __name__ == '__main__':

    try:
        args = extract_and_validate_args(sys.argv)
        calculate_one(*args)
        calculate_two(*args)
    except (SyntaxError, ValueError) as e:
        print 'right usage: axado.py <origem> <destino> <nota_fiscal> <peso>'
        print e
