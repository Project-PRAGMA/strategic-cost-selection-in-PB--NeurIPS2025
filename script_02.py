#!/usr/bin/env python3

import sys
import os


import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from _glossary import NAMES
from _utils import *
import math

from matplotlib.patches import FancyBboxPatch, Rectangle

import matplotlib.pyplot as plt
plt.rc('font', family='serif', serif='Times')
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{amsmath}')



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


def sort_by_indexes(lst, indexes, reverse=False):
    return [val for (_, val) in sorted(zip(indexes, lst), key=lambda x: \
        x[0], reverse=reverse)]


def get_supporters(profile, c):
    support = 0
    for vote in profile:
        if c.name in vote:
            support += 1
    return support


def print_margin_plot(region, name, instance, profile, rule,
                      winning_costs, winning_max_costs,
                      losing_costs, losing_max_costs, limit=1., ref_fontsize = 14,
                      ax = None):

    fig = None
    if not ax:
      fig, ax = plt.subplots(figsize=(8, 4))

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
    ordered_winning = sort_by_indexes(winning, support, True)
    ordered_support = sort_by_indexes(support, support, True)

    ## OLD VERSION ##
    if False:
        for i in range(len(ordered_costs)):
            if ordered_winning[i]:
                color = 'forestgreen'
            else:
                color = 'indianred'

            if ordered_max_costs[i] > ordered_costs[i]:
                ax.bar(i, ordered_costs[i], color=color, alpha=0.9)
                ax.bar(i, ordered_max_costs[i], color=color, alpha=0.5)
            else:
                ax.bar(i, ordered_max_costs[i], color=color, alpha=0.9)

            ax.bar(i, ordered_costs[i], fill=None, alpha=1, edgecolor='black')
    #####################################################

    for i in range(len(ordered_costs)):
        if ordered_winning[i]:
            color = 'forestgreen'
        else:
            color = 'indianred'

        if ordered_max_costs[i] > ordered_costs[i]:
            win_margin = ordered_max_costs[i] - ordered_costs[i]
            #ax.bar(i, ordered_costs[i], color=color, alpha=0.9)
            ax.bar(i, win_margin, color=color, alpha=0.35, bottom =
                   ordered_costs[i])
        else:
            lose_margin = ordered_costs[i] - ordered_max_costs[i]
            ax.bar(i, lose_margin, color=color, alpha=0.35, bottom =
                   ordered_max_costs[i])

        tick_width = 0.8
        #ax.hlines(y=ordered_max_costs[i], xmin=i - tick_width/2, xmax=i + tick_width/2, color='black', linewidth=1)
        #ax.bar(i, ordered_costs[i], fill=None, alpha=1, edgecolor='black')
        #ax.plot(i, ordered_costs[i], marker='x', markersize=3,
        #            color=(0.3, 0.3, 0.3), mew=0.5)
        ax.hlines(y=ordered_costs[i], xmin=i - tick_width/2, xmax=i + tick_width/2, color='black', linewidth=1)

        ax.plot(i, ordered_max_costs[i], marker='x', markersize=3,
                    color=(0.0, 0.0, 0.0), mew=0.6)

    ylimit_val = limit * int(instance.budget_limit) * 1.02
    scale_y = 1e6
    rounding = 0.05

    rounded_scaled_max = math.ceil((ylimit_val/scale_y)/rounding)
    #### HACK FOR PLOTTING PAPER VERSION ####
    if (not fig) and rounded_scaled_max < 3:
        rounded_scaled_max = 1
    ylimit_val = rounded_scaled_max*rounding*scale_y
    ax.set_ylim([0, ylimit_val])

    nbins = 8
    step = int((len(ordered_support) - 1) / nbins)
    ticks = [i * step for i in range(nbins + 1)]
    labels = [ordered_support[i] for i in ticks]

    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_y))
    ax.yaxis.set_major_formatter(ticks_y)

    ax.set_xticks(ticks=ticks)
    if not fig:
      xlabel_fontsize = int(ref_fontsize*11/10)
      ylabel_fontsize = int(ref_fontsize*12/10)
      title_fontsize = int(ref_fontsize*11/6)
      pad = int(ref_fontsize*4/3)
      ax.set_title(f'{nice_name.get(rule, rule)}', fontsize=title_fontsize, pad = pad)
      ax.set_xticklabels(labels=labels, rotation=45, fontsize=xlabel_fontsize)
      ax.tick_params(axis='y', labelsize=ylabel_fontsize)
    else:
      bigfontsize = 34
      tickfontsize = 24
      xylabelsfontsize = 30
      ax.set_xticklabels(labels=labels, rotation=90, fontsize=tickfontsize)
      ax.tick_params(axis='y', labelsize=tickfontsize)
      plt.xlabel('Number of votes', fontsize=xylabelsfontsize)
      plt.ylabel('Cost (in millions)', fontsize=xylabelsfontsize)

      plt.title(f'{nice_name.get(rule, rule)} | {NAMES[region][name]}',
                fontsize=bigfontsize)
      name = name.replace('.pb', '')
      os.makedirs("images", exist_ok=True)
      plt.savefig(f'images/margins/{region}/{name}_{rule}', dpi=200, bbox_inches='tight')

nice_name = {
    'mes': 'MES',
    'greedy': "Greedy",
    'greedy_cost_sat': 'BasicAV',
    'greedy_cardinality_sat': 'AV/Cost',
    'phragmen': 'Phragmén',
    'mes_phragmen': 'MES-Cost/Ph',
    'mes_card_phragmen': 'MES-Apr/Ph',
}

def plot_to_paper_neurips():
    
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


    for i, region in enumerate(['warszawa_2023', 'amsterdam']):
        for name in paper_names[region]:
            for j, rule in enumerate(paper_rules):
                winning_costs, winning_max_costs = import_values(region, name, rule, type='winning')
                losing_costs, losing_max_costs = import_values(region, name, rule, type='losing')
                instance, profile = import_election(region, name)

                print_margin_plot(region, name, instance, profile, rule,
                                  winning_costs, winning_max_costs,
                                  losing_costs, losing_max_costs,
                                  # limit=0.25
                                  # limit=0.18
                                  limit=0.21,
                                  ax=axes[i][j],
                                  ref_fontsize = basic_fontsize
                                  )

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



    legend_y_pos = -0.012
    dist_from_patch = 0.005

    stripe_wm = Rectangle((0.1, legend_y_pos), 0.05, 0.02, transform=fig.transFigure,
                   color='green', alpha=0.35, linewidth=0,  clip_on=False)
    fig.patches.append(stripe_wm)
    fig.text(0.15 + dist_from_patch, legend_y_pos + 0.007, 'Winning margin', fontsize=12, va='center', ha='left')

    stripe_lm = Rectangle((0.25, legend_y_pos), 0.05, 0.02, transform=fig.transFigure,
                   color='red', alpha=0.35, linewidth=0,  clip_on=False)
    fig.patches.append(stripe_lm)
    fig.text(0.3 + dist_from_patch, legend_y_pos + 0.007, 'Losing margin', fontsize=12, va='center', ha='left')

    legend_rect = Rectangle(
    (0.09, -0.03), 0.285, 0.055,               # (x, y), width, height in figure coords
    transform=fig.transFigure,             # position relative to the full figure
    facecolor='none',                     # no fill
    edgecolor='grey',                    # visible border
    linewidth=1,
    alpha = 0.8,
    clip_on=False
    )

    fig.patches.append(legend_rect)


    #for row_idx in range(2):
    #    # [left, bottom, width, height] in figure coordinates
    #    if row_idx == 0:
    #        # Top row
    #        bottom = 0.53
    #    else:
    #        # Bottom row
    #        bottom = 0.05

    #    box = FancyBboxPatch(
    #        (0.01, bottom),          # (x, y)
    #        0.98, 0.42,              # width, height
    #        boxstyle="round,pad=0.02,rounding_size=20",
    #        facecolor="#f0f0f0",     # light grey
    #        edgecolor='none',
    #        transform=fig.transFigure,
    #        zorder=0  # draw underneath everything
    #    )
    #fig.patches.append(box) 

    os.makedirs("images", exist_ok=True)
    fig.savefig(f'images/PAPERPLOT_margins', dpi=300, bbox_inches='tight')

def plot_to_cr_neurips():

    basic_fontsize = 40
    
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

    fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(17, 7), squeeze = False,
                             gridspec_kw={'wspace': 0.05, 'hspace': 0.25})



    regions_to_print = ['warszawa_2023', 'amsterdam']

    for i, region in enumerate(regions_to_print):
        for name in paper_names[region]:
            for j, rule in enumerate(paper_rules):
                winning_costs, winning_max_costs = import_values(region, name, rule, type='winning')
                losing_costs, losing_max_costs = import_values(region, name, rule, type='losing')
                instance, profile = import_election(region, name)

                print_margin_plot(region, name, instance, profile, rule,
                                  winning_costs, winning_max_costs,
                                  losing_costs, losing_max_costs,
                                  # limit=0.25
                                  # limit=0.18
                                  limit=0.21,
                                  ax=axes[i][j]
                                  )

    axes_labels_fonsize = int(12/20*basic_fontsize)

    for row_num, row_axes in enumerate(axes):
        row_axes[0].set_ylabel('Cost (in millions)', rotation='vertical',
         fontsize=axes_labels_fonsize)
        # Remove titles in second row
        if row_num == 1:
            for ax in row_axes:
                ax.set_title("")
        for ax in row_axes:
            ax.tick_params(axis='both', which='major', width=0.5)
            for spine in ax.spines.values():
                spine.set_linewidth(0.5)
        # Make each subplot in the row share y-axis with the first one in that row
        for ax in row_axes[1:]:
            ax.set_yticklabels(labels=[])

    fig.text(0.5, 0.038,'Number of votes', ha='center', va='top',
             fontsize=axes_labels_fonsize)

    #### MAKING LEGEND ####
    legend_fontsize = int(8/20*basic_fontsize)

    legend_y_pos = 0.005
    dist_from_patch = 0.005
    patch_width = 0.05

    stripe_wm = Rectangle((0.1, legend_y_pos), patch_width, 0.02,
                          transform=fig.transFigure, color='green', alpha=0.35,
                          linewidth=0,  clip_on=False)
    fig.patches.append(stripe_wm)
    fig.text(0.15 + dist_from_patch, legend_y_pos + 0.007, 'Winning margin',
             fontsize=legend_fontsize, va='center', ha='left')

    red_pos_x = 0.2675
    stripe_lm = Rectangle((red_pos_x, legend_y_pos), patch_width, 0.02,
                          transform=fig.transFigure, color='red', alpha=0.35,
                          linewidth=0,  clip_on=False)
    fig.patches.append(stripe_lm)
    fig.text(red_pos_x + patch_width + dist_from_patch, legend_y_pos + 0.007,
             'Losing margin', fontsize=legend_fontsize, va='center', ha='left')

    legend_rect = Rectangle(
    (0.09, -0.005), 0.3155, 0.0375,               # (x, y), width, height in figure coords
    transform=fig.transFigure,             # position relative to the full figure
    facecolor='none',                     # no fill
    edgecolor='grey',                    # visible border
    linewidth=1,
    alpha = 0.8,
    clip_on=False
    )
    fig.patches.append(legend_rect)

    os.makedirs("images", exist_ok=True)
    fig.savefig(f'images/margins_cr', dpi=300, bbox_inches='tight')



if __name__ == "__main__":

    rules = [
        'greedy_cost_sat',
        'greedy_cardinality_sat',
        'phragmen',
        'mes_phragmen',
        'mes_card_phragmen'
    ]

    paper_plot = None
    if len(sys.argv) < 2:
        regions = [
            'warszawa_2023',
            'amsterdam',
        ]
    else:
        paper_plot = sys.argv[1] == "paperplot" 
        if not paper_plot:
            regions = [str(sys.argv[1])]

    if paper_plot:
        #plot_to_paper_neurips()
        plot_to_cr_neurips()
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
                winning_costs, winning_max_costs = import_values(region, name, rule, type='winning')
                losing_costs, losing_max_costs = import_values(region, name, rule, type='losing')
                instance, profile = import_election(region, name)

                print_margin_plot(region, name, instance, profile, rule,
                                  winning_costs, winning_max_costs,
                                  losing_costs, losing_max_costs,
                                  # limit=0.25
                                  # limit=0.18
                                  limit=0.21
                                  )
