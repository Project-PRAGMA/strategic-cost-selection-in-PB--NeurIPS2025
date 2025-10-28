#!/usr/bin/env python3

import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from tqdm import tqdm

from matplotlib.patches import Polygon, Rectangle, Ellipse

from _glossary import NAMES
from _utils import *

import matplotlib.pyplot as plt
plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{amsmath}')


def compute_analytical_equilibrium_of_greedy_cost_sat(region, name):

    instance, profile = import_election(region, name)

    supporters = {}
    for p in instance:
        supporters[p] = get_supporters(profile, p)

    last_costs = {}
    for p in instance:
        if supporters[p] == max(supporters.values()):
            last_costs[p] = instance.budget_limit
        else:
            last_costs[p] = 0

    return last_costs


def compute_analytical_equilibrium_of_greedy_cardinality_sat(region, name):

    instance, profile = import_election(region, name)

    total_support = get_total_support(profile)

    last_costs = {p.name: instance.budget_limit * get_supporters(profile, p)/ total_support for p in instance}

    return last_costs


def compute_analytical_equilibrium_of_mes(region, name):

    instance, profile = import_election(region, name)

    money_unit = float(instance.budget_limit / len(profile))

    support = []
    projects = []
    for c in instance:
        support.append(get_supporters(profile, c))
        projects.append(c)
    ordered_projects = sort_by_indexes(projects, support, True)

    last_costs = {p.name: 0 for p in instance}

    q = 1
    while True:
        #print(q)
        q = q+1

        p = ordered_projects[0]

        last_cost = 0

        for i, v in enumerate(profile):

            if p.name in v:
                last_cost += money_unit
                v.clear()

        support = []
        projects = []
        for c in instance:
            support.append(get_supporters(profile, c))
            projects.append(c)
        ordered_projects = sort_by_indexes(projects, support, True)

        last_costs[p.name] = last_cost

        # print(p.name, last_cost, p.cost)

        if sum(support) == 0:
            break

    return last_costs


nice_name = {
    'mes': 'MES',
    'greedy': "Greedy",
    'greedy_cost_sat': 'BasicAV',
    'greedy_cardinality_sat': 'AV/Cost',
    'phragmen': 'Phragmén',
    'mes_phragmen': 'MES-Cost/Ph',
    'mes_card_phragmen': 'MES-Apr/Ph',
}

def import_values(region, name, method, lower_bound, r):
    name = name.replace('.pb', '')
    lower_bound = str(lower_bound).replace('.', '')
    path = f"games/{region}/{name}_{method}_{lower_bound}_{r}.csv"
    #path = f"games/{region}/{name}_{method}_{r}.csv"

    costs = {}
    last_costs = {}
    winners = {}
    with open(path, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            id_ = str(row['idx'])
            #id_ = str(row['id'])
            cost = float(row['cost'])
            last_cost = float(row['last_cost'])
            winner = int(row['winner'])
            costs[id_] = cost
            last_costs[id_] = last_cost
            winners[id_] = winner

    return costs, last_costs, winners


def paper_plot_labels(ax, rule_nicename, labels):
    ax.set_title(f'{rule_nicename}', fontsize=10)
    ax.set_xticklabels(labels=labels, rotation=45, fontsize=10)
    ax.tick_params(axis='y', labelsize=12)

def standard_plot_labels(ticks, labels):
    plt.xticks(ticks=ticks, labels=labels, rotation=90, fontsize=18)
    plt.yticks(fontsize=18)
    plt.xlabel('Number of votes', fontsize=24)
    plt.ylabel('Cost (in millions)', fontsize=24)
    plt.title(f'{nice_name.get(rule, rule)} | {NAMES[region][name]}', fontsize=28)

def setting_paperplot_limits(ax, instance, limit):
    ylimit_val = limit * int(instance.budget_limit) * 1.02
    scale_y = 1e6
    rounding = 0.05

    rounded_scaled_max = math.ceil((ylimit_val/scale_y)/rounding)
    #### HACK FOR PLOTTING PAPER VERSION ####
    if rounded_scaled_max < 3:
        rounded_scaled_max = 1
    if rounded_scaled_max > 5:
        rounded_scaled_max = 5
    ylimit_val = rounded_scaled_max*rounding*scale_y
    ax.set_ylim([0, ylimit_val])

def plotting_values(ax, ordered_costs, ordered_winners, ordered_max_costs,
                    ordered_original_winners, instance, ordered_eq_costs, paperplot):

    msize = int(280/len(ordered_costs))**2

    if paperplot:
        msize = 4

    tshift = instance.budget_limit * (-0.0005 + int(280/len(ordered_costs))/2000)

    #### OLD VERSION
    if False:
        for i in range(len(ordered_costs)):
            if ordered_winners[i]:
                color = 'forestgreen'
            else:
                color = 'indianred'

            if ordered_max_costs[i] > ordered_costs[i]:
                ax.bar(i, ordered_costs[i], color=color, alpha=0.9)
                ax.bar(i, ordered_max_costs[i], color=color, alpha=0.5)
            else:
                ax.bar(i, ordered_max_costs[i], color=color, alpha=0.9)

            ax.bar(i, ordered_costs[i], fill=None, alpha=1, edgecolor='black')

            if ordered_original_winners[i]:
                ax.scatter(i, ordered_costs[i]+tshift, marker="^", alpha=1, color="black", s=msize)

            if ordered_eq_costs:
                ax.scatter(i, ordered_eq_costs[i], marker="o", alpha=1, color="peru", s=msize)
                ax.scatter(i, ordered_eq_costs[i], marker="o", alpha=1, color="black", s=msize/16)
    #############################


    for i in range(len(ordered_costs)):
        if ordered_winners[i]:
            color = 'forestgreen'
        else:
            color = 'indianred'


        tack_width = 0.8
        if ordered_max_costs[i] > ordered_costs[i]:
            ax.bar(i, ordered_costs[i], color=color, alpha=0.75)
            ax.bar(i, ordered_max_costs[i], color=color, alpha=0.35)
        else:
            ax.bar(i, ordered_max_costs[i], color=color, alpha=0.75)

        ax.plot([i, i], [0, ordered_costs[i]], linestyle='--', color='black', linewidth
                = 0.5)
        ax.plot([i - tack_width / 2, i + tack_width / 2], [ordered_costs[i],
                                                           ordered_costs[i]],
                color='black', linewidth = 0.5)

        #ax.bar(i, ordered_costs[i], fill=None, alpha=1, edgecolor='black')

        if ordered_original_winners[i]:
            #ax.scatter(i, -0.5, marker="^", alpha=1, color="black", s=msize)
            triangle_x_base = 0.8
            triangle_y_base = 1
            triangle_height = 0.1
            triangle = Polygon([[i, triangle_y_base - triangle_height],
                                [i - triangle_x_base / 2, triangle_y_base],
                                [i + triangle_x_base / 2, triangle_y_base]],
                               facecolor=(0.6, 0.6, 0.6), edgecolor='none', 
                               transform=ax.get_xaxis_transform(), clip_on=False)
            
            ax.add_patch(triangle)


        if ordered_eq_costs:
            ax.scatter(i, ordered_eq_costs[i], marker="o", alpha=1, color="peru", s=msize)
            ax.scatter(i, ordered_eq_costs[i], marker="o", alpha=1, color="black",
                       s=msize/18)



def print_game_plot(region, name, instance, profile, _costs, _last_costs,
                    _original_winners, _winners, rule, lower_bound, r, _eq_costs,
                    limit=1., ax=None):

    fig = None
    if not ax:
      fig, ax = plt.subplots(figsize=(8, 4))

    support = []
    costs = []
    last_costs = []
    winners = []
    original_winners = []
    eq_costs = []

    for c in instance:
        support.append(get_supporters(profile, c))
        winners.append(_winners[c.name])
        original_winners.append(_original_winners[c.name])
        costs.append(_costs[c.name])
        last_costs.append(_last_costs[c.name])
        eq_costs.append(_eq_costs[c.name])

    ordered_costs = sort_by_indexes(costs, support, True)
    ordered_max_costs = sort_by_indexes(last_costs, support, True)
    ordered_winners = sort_by_indexes(winners, support, True)
    ordered_original_winners = sort_by_indexes(original_winners, support, True)
    ordered_eq_costs = sort_by_indexes(eq_costs, support, True)
    ordered_support = sort_by_indexes(support, support, True)



    plotting_values(ax, ordered_costs, ordered_winners, ordered_max_costs,
                    ordered_original_winners, instance, ordered_eq_costs, paperplot =
                    fig == None)


    MAX_COST = int(instance.budget_limit)
    plt.ylim([0, limit*MAX_COST*1])

    if not fig:
        setting_paperplot_limits(ax, instance, limit)


    nbins = 8
    step = int((len(ordered_support)-1)/nbins)
    ticks = [i*step for i in range(nbins+1)]
    labels = [ordered_support[i] for i in ticks]

    scale_y = 1e6
    ticks_y = ticker.FuncFormatter(lambda y, pos: '{0:g}'.format(y / scale_y))
    ax.yaxis.set_major_formatter(ticks_y)


    ax.set_xticks(ticks=ticks, labels=labels, rotation=90, fontsize=18)
    

    if not fig:
        rule_nicename = nice_name.get(rule, rule)
        paper_plot_labels(ax, rule_nicename, labels)
    else:
        standard_plot_labels(ticks, labels)
        name = name.replace('.pb', '')
        lower_bound = str(lower_bound).replace('.', '')
        #plt.savefig(f'images/games/{region}/{name}_{rule}_{r}', dpi=200, bbox_inches='tight')
        dirr = os.path.join("images", "games", f"{region}")
        os.makedirs(dirr, exist_ok=True)
        plt.savefig(f'{dirr}/{name}_{rule}_{lower_bound}_{r}', dpi=200,
                    bbox_inches='tight')
        plt.close()




def print_game_plot_with_none(region, name, instance, profile, _costs, _last_costs,
                    _original_winners, _winners, rule, lower_bound, r, limit=1., ax =
                              None):
    fig = None
    if not ax:
      fig, ax = plt.subplots(figsize=(8, 4))

    support = []
    costs = []
    last_costs = []
    winners = []
    original_winners = []

    for c in instance:
        support.append(get_supporters(profile, c))
        winners.append(_winners[c.name])
        original_winners.append(_original_winners[c.name])
        costs.append(_costs[c.name])
        last_costs.append(_last_costs[c.name])

    ordered_costs = sort_by_indexes(costs, support, True)
    ordered_max_costs = sort_by_indexes(last_costs, support, True)
    ordered_winners = sort_by_indexes(winners, support, True)
    ordered_original_winners = sort_by_indexes(original_winners, support, True)
    ordered_support = sort_by_indexes(support, support, True)

    plotting_values(ax, ordered_costs, ordered_winners, ordered_max_costs,
                    ordered_original_winners, instance, ordered_eq_costs = None,
                    paperplot = fig == None)

    MAX_COST = int(instance.budget_limit)
    ax.set_ylim([0, limit*MAX_COST])

    if not fig:
        setting_paperplot_limits(ax, instance, limit)

    nbins = 8
    step = int((len(ordered_support)-1)/nbins)
    ticks = [i*step for i in range(nbins+1)]
    labels = [ordered_support[i] for i in ticks]

    scale_y = 1e6
    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_y))
    ax.yaxis.set_major_formatter(ticks_y)

    ax.set_xticks(ticks=ticks, labels=labels, rotation=90, fontsize=18)
    

    if not fig:
        rule_nicename = nice_name.get(rule, rule)
        paper_plot_labels(ax, rule_nicename, labels)
    else:
        standard_plot_labels(ticks, labels)
        name = name.replace('.pb', '')
        lower_bound = str(lower_bound).replace('.', '')
        dirr = os.path.join("images", "games", f"{region}")
        os.makedirs(dirr, exist_ok=True)
        plt.savefig(f'{dirr}/{name}_{rule}_{lower_bound}_{r}', dpi=200,
                    bbox_inches='tight')
        #plt.savefig(f'images/games/{region}/{name}_{rule}_{r}', dpi=200, bbox_inches='tight')
        plt.close()


def plot_to_paper_neurips():
    lower_bound = 0.8
    regions = ["warszawa_2023", "amsterdam"]

    paper_names = {}

    paper_names['amsterdam'] = {
        '166.pb': 'Kleine Wereld',
    }
    
    paper_names['warszawa_2023'] = {
        'poland_warszawa_2023_wesola.pb': 'Wesola',
    }

    paper_rules = [
        'greedy_cost_sat',
        'phragmen',
        'greedy_cardinality_sat',
        'mes_phragmen'
    ]

    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(17, 4))

    for i,region in enumerate(regions):

        boxplots = []
        labels = []
        budget_ratios = []
        medians = []
        ds = []

        for name in paper_names[region]:
            print(name)
            for j, rule in enumerate(paper_rules):

                ax = axes[i][j]

                instance, profile = import_election(region, name)
                original_winners_list = compute_winners(instance, profile, rule)
                original_winners = {}
                for p in instance:
                    if p in original_winners_list:
                        original_winners[p.name] = 1
                    else:
                        original_winners[p.name] = 0


                for r in tqdm(range(num_rounds+1)):

                    r = num_rounds

                    if r % 10 ==  0:

                        costs, last_costs, winners = import_values(region, name, rule, lower_bound, r)

                        if rule == 'mes_phragmen':
                            eq_costs = compute_analytical_equilibrium_of_mes(region, name)
                        elif rule == 'greedy_cardinality_sat':
                            eq_costs = compute_analytical_equilibrium_of_greedy_cardinality_sat(region, name)
                        elif rule == 'greedy_cost_sat':
                            eq_costs = compute_analytical_equilibrium_of_greedy_cost_sat(region, name)
                        else:
                            eq_costs = None

                        if eq_costs is None:
                            print_game_plot_with_none(region, name, instance, profile,
                                            costs, last_costs, original_winners, winners,
                                            rule, lower_bound, r,
                                            limit=0.25, ax = ax # Warsaw | Wesola
                                            # limit=0.18  # Amsterdam
                                            # limit = 0.21
                                            )
                        else:
                            print_game_plot(region, name, instance, profile,
                                            costs, last_costs, original_winners, winners,
                                            rule, lower_bound, r,
                                            eq_costs,
                                            limit=0.25, ax=ax # Warsaw | Wesola
                                            # limit=0.18  # Amsterdam
                                            # limit = 0.21
                                            )

                    break


    # Share y-axis *within each row*
    for row_num, row_axes in enumerate(axes):
        # Make each subplot in the row share y-axis with the first one in that row
        for ax in row_axes[1:]:
            ax.set_yticklabels(labels=[], fontsize = 12)
            ax.sharey(row_axes[0])
        if row_num == 1:
            for ax in row_axes:
                ax.set_title("")
        for ax in row_axes:
            ax.tick_params(axis='both', which='major', width=0.5)
            for spine in ax.spines.values():
                spine.set_linewidth(0.5)

    #plt.xticks(ticks=ticks, labels=labels, rotation=90, fontsize=18)
    #plt.yticks(fontsize=18)
    fig.text(0.5, 0.02,'Number of votes', ha='center', va='top', fontsize=14)
    fig.text(0.01, 11/16,'Wesola', va='center', rotation='vertical',
             fontsize=18)
    fig.text(0.025, 11/16,'(Budget: $1 001$k PLN)', va='center', rotation='vertical',
             fontsize=12)
    fig.text(0.042, 11/16,'Cost (in millions)', va='center', rotation='vertical',
             fontsize=14)
    fig.text(0.01, 4/16,'Kleine Wereld', va='center', rotation='vertical',
             fontsize=18)
    fig.text(0.025, 4/16,'(Budget: $250$k EUR)', va='center', rotation='vertical',
             fontsize=12)
    fig.text(0.042, 2/8,'Cost (in millions)', va='center', rotation='vertical',
             fontsize=14)

    plt.subplots_adjust(hspace=9/32)  # Try 0.5, 1.0, etc.
    plt.subplots_adjust(wspace=5/32)  # Try 0.5, 1.0, etc.
    plt.subplots_adjust(left=5/64)  # Default is ~0.125; smaller = less margin

    legend_y_pos = -0.02
    dist_from_patch = 0.004

    triangle_x_base = 0.004
    triangle_height = 0.035
    triangle_y_base = legend_y_pos + triangle_height
    triangle_left_start = 0.075
    triangle = Polygon([[triangle_left_start + triangle_x_base / 2, triangle_y_base - triangle_height],
                       [triangle_left_start, triangle_y_base],
                       [triangle_left_start + triangle_x_base, triangle_y_base]],
                      facecolor=(0.6, 0.6, 0.6), edgecolor='none', 
                      transform=fig.transFigure, clip_on=False)

    fig.patches.append(triangle)

    left_beg_of_first_label = triangle_left_start + triangle_x_base + dist_from_patch
    fig.text(left_beg_of_first_label, legend_y_pos +
             0.015, 'Originally winning project', fontsize=12, va='center', ha='left')

    

    xy_fig_ratio = fig.get_figwidth() / fig.get_figheight()  
    circ_height = 0.035
    eq_marker_legend_xpos =  left_beg_of_first_label + 0.1175
    big_dot = Ellipse((eq_marker_legend_xpos, legend_y_pos + 0.016), height=circ_height,
                     width=circ_height*1/xy_fig_ratio, color='peru',
                     zorder=2, transform=fig.transFigure, clip_on = False)
    ax.add_patch(big_dot)
    
    small_dot = Ellipse((eq_marker_legend_xpos, legend_y_pos + 0.016),
                        height=circ_height*0.4,
                     width=circ_height*0.4*1/xy_fig_ratio,
                       color='black', zorder=3, transform=fig.transFigure, clip_on = False)
    ax.add_patch(small_dot)

    fig.text(eq_marker_legend_xpos + 2*dist_from_patch, legend_y_pos + 0.015, "Equilibrium cost (for rules for which can be computed)", fontsize=12, va='center', ha='left')

    legend_rect = Rectangle(
    (0.065, -0.03), 0.371, 0.055,              
    transform=fig.transFigure,             # position relative to the full figure
    facecolor='none',                     # no fill
    edgecolor='grey',                    # visible border
    linewidth=1,
    alpha = 0.8,
    clip_on=False
    )

    fig.patches.append(legend_rect)

    os.makedirs("images", exist_ok=True)
    fig.savefig(f'images/PAPERPLOT_games', dpi=300, bbox_inches='tight')



if __name__ == "__main__":

    num_rounds = 10000

    lower_bound = 0.8

    rules = [
        'greedy_cost_sat',
        'greedy_cardinality_sat',
        'phragmen',
        'mes_phragmen',
        'mes_card_phragmen',
            ]

    paper_plot = None
    if len(sys.argv) < 2:
        regions = [
            'warszawa_2023',
            # 'amsterdam',
        ]
    else:
        paper_plot = sys.argv[1] == "paperplot" 
        if not paper_plot:
            regions = [str(sys.argv[1])]

    if paper_plot:
        plot_to_paper_neurips()
        exit(0)

    for region in regions:

        boxplots = []
        labels = []
        budget_ratios = []
        medians = []
        ds = []

        for i, name in enumerate(NAMES[region]):
            print(name)
            for rule in rules:

                instance, profile = import_election(region, name)
                original_winners_list = compute_winners(instance, profile, rule)
                original_winners = {}
                for p in instance:
                    if p in original_winners_list:
                        original_winners[p.name] = 1
                    else:
                        original_winners[p.name] = 0

                for r in tqdm(range(num_rounds+1)):

                    r = num_rounds

                    if r % 10 == 0:

                        costs, last_costs, winners = import_values(region, name, rule, lower_bound, r)

                        if rule == 'mes_phragmen':
                            eq_costs = compute_analytical_equilibrium_of_mes(region, name)
                        elif rule == 'greedy_cardinality_sat':
                            eq_costs = compute_analytical_equilibrium_of_greedy_cardinality_sat(region, name)
                        elif rule == 'greedy_cost_sat':
                            eq_costs = compute_analytical_equilibrium_of_greedy_cost_sat(region, name)
                        else:
                            eq_costs = None

                        if eq_costs is None:
                            print_game_plot_with_none(region, name, instance, profile,
                                            costs, last_costs, original_winners, winners,
                                            rule, lower_bound, r,
                                            limit=0.25 # Warsaw | Wesola
                                            # limit=0.18  # Amsterdam
                                            # limit = 0.21
                                            )
                        else:
                            print_game_plot(region, name, instance, profile,
                                            costs, last_costs, original_winners, winners,
                                            rule, lower_bound, r,
                                            eq_costs,
                                            limit=0.25 # Warsaw | Wesola
                                            # limit=0.18  # Amsterdam
                                            # limit = 0.21
                                            )

                    break
