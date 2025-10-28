#!/usr/bin/env python3

import os
import sys

import numpy as np
from tqdm import tqdm

from _glossary import *
from _utils import *


def import_original_winners(projects):
    winners = set()
    for project_id in projects:
        if projects[project_id]['selected'] == '1':
            winners.add(project_id)
    return winners


def convert_winners(winners):
    new_winners = set()
    for w in winners:
        new_winners.add(w.idx)
    return new_winners


def verify_cost(winners):
    total = 0
    for w in winners:
        total += w.cost
    print(total)


def _store_game_results_in_csv(region, name, method, lower_bound, results, add=''):
    name = name.replace('.pb', '')
    lower_bound = str(lower_bound).replace('.', '')
    dirr = os.path.join(os.getcwd(), "games", region)
    os.makedirs(dirr, exist_ok=True)
    path = os.path.join(dirr, f'{name}_{method}_{lower_bound}_{add}.csv')
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["idx", "cost", "last_cost", "winner"])

        for r in results:
            writer.writerow([r,
                  results[r]['cost'],
                  results[r]['last_cost'],
                  results[r]['winner']])



def compute_iterative_game(region, name, method, num_rounds=100, lower_bound=0.):

    instance, profile = import_election(region, name)

    results = {p.name: {'cost': p.cost, 'winner': 0} for p in instance}

    initial_cost = {p.name: p.cost for p in instance}

    winners_default = compute_winners(instance, profile, method)


    STEP = 0.1  # 10%
    PRECISION = 100
    MAX_COST = instance.budget_limit

    num_projects = len(instance)

    for r in tqdm(range(num_rounds)):

        if r%10 == 0:

            for p in instance:
                results[p.name]['last_cost'] = p.cost

            for p in instance:
                if p.name in winners_default:
                    results[p.name]['winner'] = 1
                else:
                    results[p.name]['winner'] = 0

            _store_game_results_in_csv(region,
                                       name,
                                       method,
                                       lower_bound,
                                       results,
                                       add=str(r))

        winners_default = compute_winners(instance, profile, method)

        instance_list = [p for p in instance]
        c = np.random.choice(instance_list, 1)[0]

        original_c_cost = c.cost

        if c.name in winners_default and c.cost != MAX_COST:

            r_step = np.random.random()*STEP
            increase = int(max(100, c.cost * r_step))
            c.cost += increase

            if c.cost > MAX_COST:
                c.cost = MAX_COST

            winners_tmp = compute_winners(instance, profile, method)

            if c.name not in winners_tmp:
                c.cost = original_c_cost

        elif c.name not in winners_default and c.cost != 1:

            r_step = np.random.random() * STEP
            decrease = int(max(100, c.cost * r_step))
            c.cost -= decrease

            if c.cost <= lower_bound * initial_cost[c.name]:
                c.cost = int(lower_bound * initial_cost[c.name])

    for p in instance:
        results[p.name]['last_cost'] = p.cost

    _store_game_results_in_csv(region, name, method, lower_bound, results, add=str(num_rounds))


if __name__ == "__main__":

    lower_bound = 0.8

    num_rounds = 10000

    if len(sys.argv) >= 2:
        regions = [str(sys.argv[1])]
    else:
        regions = [
            'warszawa_2023',
            'amsterdam',
        ]

    for region in regions:

        if len(sys.argv) >= 3:
            names = [str(sys.argv[2])]
        else:
            names = NAMES[region]

        for name in names:

            compute_iterative_game(region, name, 'greedy_cost_sat',
                                   num_rounds=num_rounds, lower_bound=lower_bound)
            compute_iterative_game(region, name, 'greedy_cardinality_sat',
                                   num_rounds=num_rounds, lower_bound=lower_bound)
            compute_iterative_game(region, name, 'phragmen',
                                   num_rounds=num_rounds, lower_bound=lower_bound)
            compute_iterative_game(region, name, 'mes_phragmen',
                                   num_rounds=num_rounds, lower_bound=lower_bound)
            compute_iterative_game(region, name, 'mes_card_phragmen',
                                   num_rounds=num_rounds, lower_bound=lower_bound)
