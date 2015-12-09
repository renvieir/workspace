from myexceptions import LimitExceededError
import sys
import csv
import os
import math


def extract_and_validate_args(args):
    if len(args) != 5:
        raise Exception('right usage: axado.py <origem> <destino> <nf> <peso>')

    if not isinstance(args[1], str):
        raise ValueError('<origem> must be string')

    if not isinstance(args[2], str):
        raise ValueError('<destino> must be string')

    try:
        nf = float(args[3])
    except:
        raise ValueError('<nf> must be integer')

    try:
        peso = float(args[4])
    except:
        raise ValueError('<peso> must be integer')

    return [args[1], args[2], nf, peso]


def parse_rota_csv(origin, destination, filename, delimiter=','):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        reader.next()
        for line in reader:
            if line[0] != origin or line[1] != destination:
                continue
            else:
                line[2] = int(line[2])
                line[3] = int(line[3])
                line[-1] = int(line[-1])
                return line

    raise Exception('Route not Found!')


def parse_preco_csv(nome, peso, filename, delimiter=','):
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
                    line[-1] = float(line[-1])
                    return line

                if begin <= peso and peso < end:
                    line[-1] = float(line[-1])
                    return line
                else:
                    continue

    raise Exception('Price not Found!')


def parse_rota_tsv(origin, destination, weight, filename):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        reader.next()
        for line in reader:
            limit = int(line[2])
            if limit > 0 and weight > limit:
                raise LimitExceededError

            if line[0] != origin or line[1] != destination:
                continue
            else:
                for i in range(2, 7):
                    line[i] = int(line[i])
                return line

    raise Exception('Route not Found!')


def parse_preco_tsv(nome, peso, filename):
    return parse_preco_csv(nome, peso, filename, delimiter='\t')


def calculate_one(origin, detination, nf, weight):
    dirs = ['tabela', 'tabela2']

    rotas_path = os.path.join(dirs[0], 'rotas.csv')
    preco_path = os.path.join(dirs[0], 'preco_por_kg.csv')

    ori, dest, prazo, seguro, kg, fixa = parse_rota_csv(origin, detination, rotas_path)
    nome, ini, fin, preco = parse_preco_csv(kg, weight, preco_path)

    seguro = (nf * seguro) / 100.0
    faixa = weight * preco
    subtotal = seguro + fixa + faixa
    taxa_icms = 6.0

    total = subtotal / ((100.0 - taxa_icms) / 100.0)

    print '{0}:{1}, {2}'.format('tabela', prazo, round(total + .005, 2))


def calculate_two(origin, detination, nf, weight):
    dirs = ['tabela', 'tabela2']

    rotas_path = os.path.join(dirs[1], 'rotas.tsv')
    preco_path = os.path.join(dirs[1], 'preco_por_kg.tsv')

    try:
        origem, destino, limite, prazo, seguro, icms, alfandega, kg = parse_rota_tsv(origin, detination, weight, rotas_path)
    except LimitExceededError as e:
        print '{0}:{1}, {2}'.format('tabela2', '-', '-')
        return

    nome, ini, fin, preco = parse_preco_tsv(kg, weight, preco_path)

    seguro = nf * seguro / 100.0
    faixa = weight * preco
    subtotal = seguro + faixa

    total_alfandega = subtotal * (alfandega / 100.0)
    subtotal += total_alfandega

    total = subtotal / ((100.0 - icms) / 100.0)

    print '{0}:{1}, {2}'.format('tabela2', prazo, round(total + .005, 2))


if __name__ == '__main__':

    try:
        args = extract_and_validate_args(sys.argv)
        calculate_one(*args)
        calculate_two(*args)
        '''
        if(validate_args(sys.argv)):
            print 'That is right'
        read_csv(os.path.join('tabela','rotas.csv'))
        read_tsv(os.path.join('tabela2','rotas.tsv'))
        '''
    except Exception as e:
        import traceback

        print traceback.print_exc()
