import csv
import os
from _glossary import NAMES
import sys
import statistics
import ast
from _utils import *

import matplotlib.pyplot as plt
import numpy as np

from scipy import stats
import matplotlib.ticker as ticker

nice_name = {

    'mes': 'MES',
    'greedy': "Greedy",
    'greedy_cost_sat': 'BasicAV',
    'greedy_cardinality_sat': 'AV/Cost',
    'phragmen': 'Phragmén',
    'mes_phragmen': 'MES-Cost/Ph',
    'mes_card_phragmen': 'MES-Apr/Ph',

}


def import_values(region, name, method, limit=10, type=None):
    name = name.replace('.pb', '')
    path = f"margins/{type}/{region}/{name}_{method}.csv"

    costs = {}
    max_costs = {}
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            id_ = str(row['idx'])
            cost = float(row['cost'])
            max_cost = float(row['max_cost'])
            costs[id_] = cost
            max_costs[id_] = max_cost

    return costs, max_costs

def import_values_game(region, name, method, limit=10, type=None, add=''):
    name = name.replace('.pb', '')
    path = f"margins/{type}/{region}/{name}_{method}_{add}.csv"

    costs = {}
    max_costs = {}
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            id_ = str(row['idx'])
            cost = float(row['cost'])
            max_cost = float(row['max_cost'])
            costs[id_] = cost
            max_costs[id_] = max_cost

    return costs, max_costs

def import_values_game2(region, name, method, r):
    name = name.replace('.pb', '')
    path = f"games/{region}/{name}_{method}_{r}.csv"

    costs = {}
    last_costs = {}
    winners = {}
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            id_ = str(row['idx'])
            cost = float(row['cost'])
            last_cost = float(row['last_cost'])
            winner = int(row['winner'])
            costs[id_] = cost
            last_costs[id_] = last_cost
            winners[id_] = winner

    return costs, last_costs, winners

def sort_by_indexes(lst, indexes, reverse=False):
  return [val for (_, val) in sorted(zip(indexes, lst), key=lambda x: \
          x[0], reverse=reverse)]


def get_supporters(profile, c):
    support = 0
    for vote in profile:
        if c.name in vote:
            support += 1
    return support


def print_margin_stats(region, name, instance, profile,
                              winning_costs, winning_max_costs,
                              losing_costs, losing_max_costs, rule,):
    fig, ax = plt.subplots()

    support = []
    costs = []
    max_costs = []
    winning = []

    for c in instance:
        support.append(get_supporters(profile, c))
        if c.name in winning_costs:
            winning.append(True)
            costs.append(winning_costs[c.name])
            max_costs.append(winning_max_costs[c.name])
        elif c.name in losing_costs:
            winning.append(False)
            costs.append(losing_costs[c.name])
            max_costs.append(losing_max_costs[c.name])

    ordered_costs = sort_by_indexes(costs, support, True)
    ordered_max_costs = sort_by_indexes(max_costs, support, True)

    plus = []
    minus = []

    for i in range(len(ordered_costs)):
        diff = ordered_max_costs[i] - ordered_costs[i]
        if diff > 0:
            plus.append(diff)
        elif diff < 0:
            minus.append(diff)

    plus = np.array(plus)
    minus = np.array(minus)
    line = f'${convert(np.mean(plus))} \pm {convert(np.std(plus))}$ & ' \
           f'${convert(-np.mean(minus))} \pm {convert(np.std(minus))}$'
    return line

NICE = {
    'greedy_cost_sat': '\\textbasicAV',
    'greedy_cardinality_sat': '\\textAVover',
    'phragmen': '\Phragmen',
    'mes_card_phragmen': '\\MESAP',
    'mes_phragmen':  '\\MESP',
}


if __name__ == "__main__":

    rules = [
        'greedy_cost_sat',
        'greedy_cardinality_sat',
        'phragmen',
        'mes_card_phragmen',
        'mes_phragmen',
            ]


    if len(sys.argv) < 2:
        regions = [
            'warszawa_2023',
            'amsterdam',
        ]
    else:
        regions = [str(sys.argv[1])]

    for region in regions:

        boxplots = []
        labels = []
        budget_ratios = []
        medians = []
        ds = []

        for i, name in enumerate(NAMES[region]):
            print(name)
            for rule in rules:


                # BASE

                winning_costs, winning_max_costs = import_values(region, name, rule, type='winning')
                losing_costs, losing_max_costs = import_values(region, name, rule, type='losing')

                instance, profile = import_election(region, name)

                line_1 = print_margin_stats(region, name, instance, profile,
                                  winning_costs, winning_max_costs,
                                  losing_costs, losing_max_costs, rule,
                                   )
                # GAME

                winning_costs, winning_max_costs = import_values_game(region, name, rule, type='winning',  add='10000')
                losing_costs, losing_max_costs = import_values_game(region, name, rule, type='losing',  add='10000')

                instance, profile = import_election(region, name)

                line_2 = print_margin_stats(region, name, instance, profile,
                                  winning_costs, winning_max_costs,
                                  losing_costs, losing_max_costs, rule,
                                   )

                line = f'& {NICE[rule]} & {line_1} & {line_2} \\\\'
                print(line)
