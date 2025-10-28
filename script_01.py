#!/usr/bin/env python3

import os
import sys

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


def _store_results_in_csv(region, name, method, A, B, C, type):
    name = name.replace('.pb','')
    dirr = os.path.join(os.getcwd(), "margins", type, region)
    os.makedirs(dirr, exist_ok=True)
    path = os.path.join(dirr, f'{name}_{method}.csv')
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["idx", "cost", "max_cost", "ratio", "difference"])
        for i in range(len(A)):
            writer.writerow([A[i], B[i], C[i], float(C[i] / B[i]), C[i] - B[i]])



def compute_winning_margins(region, name, method):
    A = []
    B = []
    C = []

    instance, profile = import_election(region, name)

    winners_default = compute_winners(instance, profile, method)

    PRECISION = 100
    MAX_COST = instance.budget_limit

    for c in tqdm(instance):

        if c.name in winners_default:

            original_c_cost = c.cost

            left = c.cost
            right = MAX_COST

            while right - left > PRECISION:

                c.cost = int(left + (right - left) / 2)

                winners_tmp = compute_winners(instance, profile, method)

                if c.name in winners_tmp:
                    left = c.cost
                else:
                    right = c.cost

            A.append(c.name)
            B.append(original_c_cost)
            C.append(c.cost)

            c.cost = original_c_cost

    _store_results_in_csv(region, name, method, A, B, C, 'winning')


def compute_losing_margins(region, name, method):
    A = []
    B = []
    C = []

    instance, profile = import_election(region, name)

    winners_default = compute_winners(instance, profile, method)

    PRECISION = 100
    MIN_COST = 100

    for c in tqdm(instance):

        if c.name not in winners_default:

            original_c_cost = c.cost

            left = MIN_COST
            right = c.cost

            while right - left > PRECISION:

                c.cost = int(left + (right - left) / 2)

                winners_tmp = compute_winners(instance, profile, method)

                if c.name in winners_tmp:
                    left = c.cost
                else:
                    right = c.cost

            A.append(c.name)
            B.append(original_c_cost)
            C.append(c.cost)

            c.cost = original_c_cost

    _store_results_in_csv(region, name, method, A, B, C, 'losing')


if __name__ == "__main__":

    if len(sys.argv) < 2:
        regions = [
            'warszawa_2023',
            'amsterdam',
        ]
    else:
        regions = [str(sys.argv[1])]

    for region in regions:

        if len(sys.argv) >= 3:
            names = [str(sys.argv[2])]
        else:
            names = NAMES[region]

        for name in names:
            compute_winning_margins(region, name, 'greedy_cost_sat')
            compute_winning_margins(region, name, 'greedy_cardinality_sat')
            compute_winning_margins(region, name, 'phragmen')
            compute_winning_margins(region, name, 'mes_phragmen')
            compute_winning_margins(region, name, 'mes_card_phragmen')

            compute_losing_margins(region, name, 'greedy_cost_sat')
            compute_losing_margins(region, name, 'greedy_cardinality_sat')
            compute_losing_margins(region, name, 'phragmen')
            compute_losing_margins(region, name, 'mes_phragmen')
            compute_losing_margins(region, name, 'mes_card_phragmen')


