import copy
import csv
import math

from pabutools.election import Cost_Sat, Cardinality_Sat
from pabutools.election import parse_pabulib
from pabutools.rules import completion_by_rule_combination
from pabutools.rules import exhaustion_by_budget_increase
from pabutools.rules import greedy_utilitarian_welfare, method_of_equal_shares, sequential_phragmen


def mes(instance, profile):
    return completion_by_rule_combination(
        instance,
        profile,
        [method_of_equal_shares, sequential_phragmen],
        [
            {"sat_class": Cost_Sat}, {}
        ],
    )


def mes_phragmen(instance, profile):
    return completion_by_rule_combination(
        instance,
        profile,
        [method_of_equal_shares, sequential_phragmen],
        [
            {"sat_class": Cost_Sat}, {}
        ],
    )


def mes_card_phragmen(instance, profile):
    return completion_by_rule_combination(
        instance,
        profile,
        [method_of_equal_shares, sequential_phragmen],
        [
            {"sat_class": Cardinality_Sat}, {}
        ],
    )




def convert_winners_to_set(winners):
    winners_as_set = set()
    for w in winners:
        winners_as_set.add(w.idx)
    return winners_as_set


def compute_winners(instance, profile, method):
    instance_tmp = copy.deepcopy(instance)
    profile_tmp = copy.deepcopy(profile)

    if method == 'greedy_cost_sat':
        winners_tmp = greedy_utilitarian_welfare(instance_tmp, profile_tmp, sat_class=Cost_Sat)
    elif method == 'greedy_cardinality_sat':
        winners_tmp = greedy_utilitarian_welfare(instance_tmp, profile_tmp, sat_class=Cardinality_Sat)
    elif method == 'phragmen':
        winners_tmp = sequential_phragmen(instance_tmp, profile_tmp)
    elif method == 'mes_phragmen':
        winners_tmp = mes_phragmen(instance_tmp, profile_tmp)
    elif method == 'mes_card_phragmen':
        winners_tmp = mes_card_phragmen(instance_tmp, profile_tmp)
    elif method == 'mes_card':
        winners_tmp = method_of_equal_shares(instance_tmp, profile_tmp, sat_class=Cardinality_Sat)
    else:
        winners_tmp = None
    return winners_tmp


def import_election(region, name):
    path = f'data/{region}/{name}'
    instance, profile = parse_pabulib(path)
    return instance, profile


def import_data(path):
    meta = {}
    projects = {}
    votes = {}
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        section = ""
        header = []
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if str(row[0]).strip().lower() in ["meta", "projects", "votes"]:
                section = str(row[0]).strip().lower()
                header = next(reader)
            elif section == "meta":
                meta[row[0]] = row[1].strip()
            elif section == "projects":
                projects[row[0]] = {}
                for it, key in enumerate(header[1:]):
                    projects[row[0]][key.strip()] = row[it + 1].strip()
            elif section == "votes":
                votes[row[0]] = {}
                for it, key in enumerate(header[1:]):
                    votes[row[0]][key.strip()] = row[it + 1].strip()
    return meta, projects, votes


def equal_power(e):
    W = set()
    costW = 0
    ideal_pt = e.budget / len(e.voters)
    real_vector = {}
    remaining = set(e.profile.keys())
    cnt = 0
    while remaining:
        cnt += 1
        min_power_inequality = math.inf
        best_diff = None
        best_c = None
        for c in remaining:
            diff = {i : c.cost / len(e.profile[c]) for i in e.profile[c]}
            power_inequality = sum((real_vector.get(i, 0) + diff.get(i, 0) - ideal_pt) ** 2 for i in e.voters)
            if power_inequality < min_power_inequality:
                best_c = c
                best_diff = diff
                min_power_inequality = power_inequality
        W.add(best_c)
        costW += best_c.cost
        for i in best_diff:
            real_vector[i] = real_vector.get(i, 0) + best_diff[i]
        remaining.remove(best_c)
        remaining = set(c for c in remaining if c.cost + costW <= e.budget)
    return W


def get_total_support(profile):
    support = 0
    for vote in profile:
        support += len(vote)
    return support


def get_supporters(profile, c):
    support = 0
    for vote in profile:
        if c.name in vote:
            support += 1
    return support


def sort_by_indexes(lst, indexes, reverse=False):
  return [val for (_, val) in sorted(zip(indexes, lst), key=lambda x: \
          x[0], reverse=reverse)]


def convert(value):
    value /= 1000
    if value > 1:
        value = round(value, 0)
        value = int(value)
    else:
        value = round(value, 1)
    return f'{value}'