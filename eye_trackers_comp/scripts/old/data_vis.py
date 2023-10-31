from conf import Users, Figures, Actions, Surface, Fixations, Steps, GazePoints
from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _EXISTS, _GET_ALL_VALUES
import matplotlib.pyplot as plt
import constants as cst
from utils import _sum, centroid, distance, distance_min_block_corner
import sys

users = Users()
figures = Figures()
actions = Actions()
surfaces = Surface()
steps = Steps()

def stacked_barchart(to_plot, label, ax, bottom = []):
    x = []
    y = []
    for item in to_plot:
        x.append(item[0])
        y.append(item[1])

    if (len(bottom) <= 0):
        ax.bar(x,y,label=label)
        bottom = []
        for item in y:
            bottom.append(item)
    else:
        ax.bar(x,y,bottom=bottom,label=label)
        for i in range(len(y)):
            bottom[i] += y[i]
    return bottom



def _GET_USER_INFO(id):
    users.print_user_info(id)

def _PLOT_TIME(id):
    print("_PLOT_TIME %d" % id)

    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    coord = [[0,0], [0,1], [1,0], [1,1]]
    for figId in figures.get_figures_id_list():
        width = 0.3  # the width of the bars
        offset = -width*2
        csvfile = ("../data/%d_%s_actions.csv" % (id, figures.get_figure_name(figId)))
        table = _LOAD(csvfile)
        ax = axs[coord[figId][0], coord[figId][1]]
        ax.set_title(figures.get_figure_name(figId).capitalize())
        ax.set_xlabel('Step')
        ax.set_ylabel('Time (ms)')
        bottom = []
        for act in actions.get_actions_id_list():
            to_plot = []
            offset += width
            for step in range(0, figures.get_figure_n_steps(figId)+1):
                if _EXISTS(_GET_ALL(table, act, keyId="actionId"), step, "duration", keyId="stepId"):
                    to_plot.append([
                        step, \
                        _sum(_GET_ALL_VALUES(_GET_ALL(table, act, keyId="actionId"), step, "duration", keyId="stepId"))])
                else:
                    to_plot.append([step, 0])
            bottom = stacked_barchart(to_plot, actions.get_action_name(act),ax, bottom)
        ax.legend()
    fig.savefig("output/png/%d_PLOT_TIME.png" % id)

def _PLOT_SURFACE_TIME(id):
    print("_PLOT_SURFACE_TIME %d" % id)

    fig, axs = plt.subplots(4, 3, figsize=(30, 40))
    coord = [{0:[0,0], 1:[0,1], 2:[0,2]},\
            {0:[1,0], 1:[1,1], 2:[1,2]},\
            {0:[2,0], 1:[2,1], 2:[2,2]},\
            {0:[3,0], 1:[3,1], 2:[3,2]}]
    for figId in figures.get_figures_id_list():
        csvfile = ("../data/%d_%s_surfaces_duration.csv" % (id, figures.get_figure_name(figId)))
        table = _LOAD(csvfile)

        width = 0.3  # the width of the bars
        offset = -width*2
        for act in actions.get_actions_id_list():
            ax = axs[coord[figId][act][0], coord[figId][act][1]]
            f_name = figures.get_figure_name(figId).capitalize()
            a_name = actions.get_action_name(act).capitalize()
            ax.set_title("%s - %s" % (f_name, a_name))
            ax.set_xlabel('Step')
            ax.set_ylabel('Time (ms)')
            offset += width
            bottom = []
            for surf in surfaces.get_surfaces_id_list():
                to_plot = []
                for step in range(0, figures.get_figure_n_steps(figId)+1):
                    tmp = _GET_ALL(table, act, keyId="actionId")
                    tmp = _GET_ALL(tmp, step, keyId="stepId")
                    d = _sum(_GET_ALL_VALUES(tmp, surf, "duration", keyId="surfaceId"))
                    to_plot.append([step, d])
                # print("------------------------")
                # print(surfaces.get_surface_name(surf))
                # print("------------------------")
                # sys.exit(1)
                bottom = stacked_barchart(to_plot, surfaces.get_surface_name(surf),ax, bottom)
            ax.legend()
    fig.savefig("output/png/%d_PLOT_SURFACE_TIME.png" % id)

def _PLOT_FIXATION_NUMBER(id):
    print("_PLOT_FIXATION_NUMBER %d" % id)

    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    coord = [[0,0], [0,1], [1,0], [1,1]]

    for figId in figures.get_figures_id_list():
        csvfile = ("../data/%d_%s_fixations.csv" % (id, figures.get_figure_name(figId)))
        fixations = Fixations(csvfile)
        width = float(1/len(actions.get_actions_id_list()))
        offset = -width*2
        ax = axs[coord[figId][0], coord[figId][1]]
        ax.set_title(figures.get_figure_name(figId).capitalize())
        ax.set_xlabel('Step')
        ax.set_ylabel('#Fixations')
        ax.set_ylim(0,180)
        bottom=[]
        for act in actions.get_actions_id_list():
            to_plot = []
            offset += width
            for step in range(0, figures.get_figure_n_steps(figId)+1):
                to_plot.append([step, len(fixations.get_fixations(step, act))])
            bottom = stacked_barchart(to_plot, actions.get_action_name(act),ax, bottom)
        ax.legend()
    fig.savefig("output/png/%d_PLOT_FIXATION_NUMBER.png" % id)

def _PLOT_FIXATION_TIME(id):
    print("_PLOT_FIXATION_TIME %d" % id)
    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    coord = [[0,0], [0,1], [1,0], [1,1]]

    for figId in figures.get_figures_id_list():
        csvfile = ("../data/%d_%s_fixations.csv" % (id, figures.get_figure_name(figId)))
        fixations = Fixations(csvfile)
        ax = axs[coord[figId][0], coord[figId][1]]
        ax.set_title(figures.get_figure_name(figId).capitalize())
        ax.set_xlabel('Step')
        ax.set_ylabel('Fixations (ms)')
        ax.set_ylim(0,30000)
        first = True
        bottom = []
        for act in actions.get_actions_id_list():
            to_plot = []
            for step in range(0, figures.get_figure_n_steps(figId)+1):
                d = [fix.duration for fix in fixations.get_fixations(step, act)]
                to_plot.append([step, _sum(d)])
            bottom = stacked_barchart(to_plot, actions.get_action_name(act),ax, bottom)
            first = False
        ax.legend()
    fig.savefig("output/png/%d_PLOT_FIXATION_TIME.png" % id)

def _PLOT_FIXATION_RATIO(id):
    print("_PLOT_FIXATION_RATIO %d" % id)

    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    coord = [[0,0], [0,1], [1,0], [1,1]]

    for figId in figures.get_figures_id_list():
        csvfile = ("../data/%d_%s_fixations.csv" % (id, figures.get_figure_name(figId)))
        fixations = Fixations(csvfile)
        width = float(1/len(actions.get_actions_id_list()))
        offset = 0-(width*2)
        ax = axs[coord[figId][0], coord[figId][1]]
        ax.set_title(figures.get_figure_name(figId).capitalize())
        ax.set_xlabel('Step')
        ax.set_ylabel('Position in the right surface (\%)')
        ax.set_ylim(0,105)
        for act in actions.get_actions_id_list():
            to_plot = []
            offset += width
            for step in range(0, figures.get_figure_n_steps(figId)+1):
                surf = [fix.surface for fix in fixations.get_fixations(step, act)]
                N = len(surf)
                n = 0
                for s in surf:
                    if (act == 0 and s == 0):
                        n += 1
                    elif (act == 2 and s == 2):
                        n += 1
                    elif (act == 1 and s == steps.get_step(figId, step).get_stock_surface()):
                        n += 1
                to_plot.append([step+offset, 100*float(n/N) if N > 0 else 0])
            ax.bar(*zip(*to_plot),width,label=actions.get_action_name(act))
        ax.legend()
    fig.savefig("output/png/%d_PLOT_FIXATION_RATIO.png" % id)

def _PLOT_FIXATION_RATIO_TIME(id):
    print("_PLOT_FIXATION_RATIO_TIME %d" % id)

    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    coord = [[0,0], [0,1], [1,0], [1,1]]

    for figId in figures.get_figures_id_list():
        csvfile = ("../data/%d_%s_fixations.csv" % (id, figures.get_figure_name(figId)))
        fixations = Fixations(csvfile)
        width = float(1/len(actions.get_actions_id_list()))
        offset = 0-(width*2)
        ax = axs[coord[figId][0], coord[figId][1]]
        ax.set_title(figures.get_figure_name(figId).capitalize())
        ax.set_xlabel('Step')
        ax.set_ylabel('Position in the right surface (\%)')
        ax.set_ylim(0,105)
        for act in actions.get_actions_id_list():
            to_plot = []
            offset += width
            for step in range(0, figures.get_figure_n_steps(figId)+1):
                surf = [fix.surface for fix in fixations.get_fixations(step, act)]
                dur = [fix.duration for fix in fixations.get_fixations(step, act)]
                x = [fix.x for fix in fixations.get_fixations(step, act)]
                y = [fix.y for fix in fixations.get_fixations(step, act)]
                N = len(surf)
                n = 0
                for i in range(N):
                    if (act == 0 and surf[i] == 0):
                        n += dur[i]
                    elif (act == 2 and surf[i] == 2):
                        n += dur[i]
                    elif (act == 1 and surf[i] == steps.get_step(figId, step).get_stock_surface()):
                        n += dur[i]
                to_plot.append([step+offset, 100*float(n/_sum(dur)) if N > 0 else 0])
            ax.bar(*zip(*to_plot),width,label=actions.get_action_name(act))
        ax.legend()
    fig.savefig("output/png/%d_PLOT_FIXATION_RATIO_TIME.png" % id)

def _PLOT_FIXATION_AVG_TIME(id):
    print("_PLOT_FIXATION_AVG_TIME %d" % id)

    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    coord = [[0,0], [0,1], [1,0], [1,1]]

    for figId in figures.get_figures_id_list():
        csvfile = ("../data/%d_%s_fixations.csv" % (id, figures.get_figure_name(figId)))
        fixations = Fixations(csvfile)
        width = float(1/len(actions.get_actions_id_list()))
        offset = 0-(width*2)
        ax = axs[coord[figId][0], coord[figId][1]]
        ax.set_title(figures.get_figure_name(figId).capitalize())
        ax.set_xlabel('Step')
        ax.set_ylabel('Position in the right surface (\%)')
        ax.set_ylim(0,300)
        for act in actions.get_actions_id_list():
            to_plot = []
            offset += width
            for step in range(0, figures.get_figure_n_steps(figId)+1):
                dur = [fix.duration for fix in fixations.get_fixations(step, act)]
                to_plot.append([step+offset, _sum(dur)/len(dur) if len(dur) > 0 else 0])
            ax.bar(*zip(*to_plot),width,label=actions.get_action_name(act))
        ax.legend()
    fig.savefig("output/png/%d_PLOT_FIXATION_AVG_TIME.png" % id)

def _PLOT_FIXATION_DISPERSION(id):
    print("_PLOT_FIXATION_DISPERSION %d" % id)

    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    coord = [[0,0], [0,1], [1,0], [1,1]]

    for figId in figures.get_figures_id_list():
        csvfile = ("../data/%d_%s_fixations.csv" % (id, figures.get_figure_name(figId)))
        fixations = Fixations(csvfile)
        width = float(1/len(actions.get_actions_id_list()))
        offset = -width*2
        ax = axs[coord[figId][0], coord[figId][1]]
        ax.set_title(figures.get_figure_name(figId).capitalize())
        ax.set_xlabel('Step')
        ax.set_ylabel('#Fixations')
        ax.set_ylim(0,1)
        for act in actions.get_actions_id_list():
            to_plot = []
            offset += width
            for step in range(0, figures.get_figure_n_steps(figId)+1):
                x = [fix.x for fix in fixations.get_fixations(step, act)]
                y = [fix.y for fix in fixations.get_fixations(step, act)]
                positions = [p for p in list(zip(x,y))]
                if(len(positions) > 0):
                    c = centroid(positions)
                    dist = [distance(p,c) for p in positions]
                    to_plot.append([step+offset, float(_sum(dist)/len(dist))])
            ax.bar(*zip(*to_plot),width,label=actions.get_action_name(act))
        ax.legend()
    fig.savefig("output/png/%d_PLOT_FIXATION_DISPERSION.png" % id)

def _PLOT_FIXATION_DISPERSION_MM(id):
    print("_PLOT_FIXATION_DISPERSION_MM %d" % id)

    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    coord = [[0,0], [0,1], [1,0], [1,1]]

    for figId in figures.get_figures_id_list():
        csvfile = ("../data/%d_%s_fixations.csv" % (id, figures.get_figure_name(figId)))
        fixations = Fixations(csvfile)
        width = float(1/len(actions.get_actions_id_list()))
        offset = -width*2
        ax = axs[coord[figId][0], coord[figId][1]]
        ax.set_title(figures.get_figure_name(figId).capitalize())
        ax.set_xlabel('Step')
        ax.set_ylabel('Dispersion (mm)')
        ax.set_ylim(0,70)
        for act in actions.get_actions_id_list():
            if(act == 0):
                continue
            to_plot = []
            offset += width
            for step in range(0, figures.get_figure_n_steps(figId)+1):
                s = [fix.surface for fix in fixations.get_fixations(step, act)]
                x = [fix.x for fix in fixations.get_fixations(step, act)]
                y = [fix.y for fix in fixations.get_fixations(step, act)]
                positions = []
                for i in range(len(s)):
                    p = [x[i], y[i]]
                    if (act == 2 and s[i] == 2):
                        positions.append(surfaces.get_absolute_coordinates(s[i], p))
                    elif (act == 1 and (s[i] == 1 or s[i] == 3)):
                        positions.append(surfaces.get_absolute_coordinates(s[i], p))
#                     print("(%f %f) (%f %f)" %(p[0], p[1], surfaces.get_absolute_coordinates(s[i], p)[0], surfaces.get_absolute_coordinates(s[i], p)[1]))
                if(len(positions) > 0):
                    c = centroid(positions)
                    dist = [distance(p,c) for p in positions]
                    to_plot.append([step+offset, float(_sum(dist)/len(dist))])
            ax.bar(*zip(*to_plot),width,label=actions.get_action_name(act))
        ax.legend()
    fig.savefig("output/png/%d_PLOT_FIXATION_DISPERSION_MM.png" % id)

def _PLOT_FIXATION_DISTANCE(id):
    print("_PLOT_FIXATION_DISTANCE %d" % id)

    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    coord = [[0,0], [0,1], [1,0], [1,1]]

    for figId in figures.get_figures_id_list():
        csvfile = ("../data/%d_%s_fixations.csv" % (id, figures.get_figure_name(figId)))
        fixations = Fixations(csvfile)
        width = float(1/(len(actions.get_actions_id_list())-1))
        offset = -width*2
        ax = axs[coord[figId][0], coord[figId][1]]
        ax.set_title(figures.get_figure_name(figId).capitalize())
        ax.set_xlabel('Step')
        ax.set_ylabel('Distance (mm)')
        ax.set_ylim(0,150)
        for act in actions.get_actions_id_list():
            if(act == 0):
                continue
            to_plot = []
            offset += width
            for step in range(1, figures.get_figure_n_steps(figId)+1):
                s = [fix.surface for fix in fixations.get_fixations(step, act)]
                x = [fix.x for fix in fixations.get_fixations(step, act)]
                y = [fix.y for fix in fixations.get_fixations(step, act)]
                positions = []
                step_to_achieve = steps.get_step(figId, step)
                for i in range(len(s)):
                    p = [x[i], y[i]]
                    if (act == 2 and s[i] == 2):
                        positions.append(surfaces.get_absolute_coordinates(s[i], p))
                    elif (act == 1 and s[i] == step_to_achieve.get_stock_surface()):
                        positions.append(surfaces.get_absolute_coordinates(s[i], p))
#                     print("(%f %f) (%f %f)" %(p[0], p[1], surfaces.get_absolute_coordinates(s[i], p)[0], surfaces.get_absolute_coordinates(s[i], p)[1]))
                if(len(positions) > 0):
                    if(act == 1):
                        # Pick case
                        # print(step_to_achieve.block.position)
                        block_to_pick = step_to_achieve.block.position
                        # print(block_to_pick)
                        block_to_pick = [surfaces.get_norm_coordinates(\
                                        step_to_achieve.get_stock_surface(),\
                                        p) for p in block_to_pick]
                        # print(block_to_pick)
                        block_to_pick = [surfaces.get_absolute_coordinates(\
                                        step_to_achieve.get_stock_surface(),\
                                        p) for p in block_to_pick]
                        # print(block_to_pick)
                        # print(positions)
                        dist = [distance_min_block_corner(p,block_to_pick) for p in positions]
                        to_plot.append([step+offset, float(_sum(dist)/len(dist))])
                    if(act == 2):
                        # print(step_to_achieve.block.position)
                        position_to_place = step_to_achieve.position_to_place
                        # print(block_to_pick)
                        position_to_place = [surfaces.get_norm_coordinates(\
                                        step_to_achieve.get_stock_surface(),\
                                        p) for p in position_to_place]
                        # print(block_to_pick)
                        position_to_place = [surfaces.get_absolute_coordinates(\
                                        step_to_achieve.get_stock_surface(),\
                                        p) for p in position_to_place]
                        # print(block_to_pick)
                        # print(positions)
                        dist = [distance_min_block_corner(p,position_to_place) for p in positions]
                        to_plot.append([step+offset, float(_sum(dist)/len(dist))])
                    else:
                        to_plot.append([step+offset, 0])

            ax.bar(*zip(*to_plot),width,label=actions.get_action_name(act))
        ax.legend()
    fig.savefig("output/png/%d_PLOT_FIXATION_DISTANCE.png" % id)


def _PLOT_FIXATION_DISTANCE_RATIO(id, thresh):
    print("_PLOT_FIXATION_DISTANCE %d" % id)

    fig, axs = plt.subplots(2, 2, figsize=(15, 15))
    coord = [[0,0], [0,1], [1,0], [1,1]]

    for figId in figures.get_figures_id_list():
        csvfile = ("../data/%d_%s_fixations.csv" % (id, figures.get_figure_name(figId)))
        fixations = Fixations(csvfile)
        width = float(1/(len(actions.get_actions_id_list())-1))
        offset = -width
        ax = axs[coord[figId][0], coord[figId][1]]
        ax.set_title(figures.get_figure_name(figId).capitalize())
        ax.set_xlabel('Step')
        ax.set_ylabel('Distance (mm)')
        ax.set_ylim(0,105)
        for act in actions.get_actions_id_list():
            if(act == 0):
                continue
            to_plot = []
            offset += width
            for step in range(1, figures.get_figure_n_steps(figId)+1):
                s = [fix.surface for fix in fixations.get_fixations(step, act)]
                x = [fix.x for fix in fixations.get_fixations(step, act)]
                y = [fix.y for fix in fixations.get_fixations(step, act)]
                positions = []
                step_to_achieve = steps.get_step(figId, step)
                for i in range(len(s)):
                    p = [x[i], y[i]]
                    if (act == 2 and s[i] == 2):
                        positions.append(surfaces.get_absolute_coordinates(s[i], p))
                    elif (act == 1 and s[i] == step_to_achieve.get_stock_surface()):
                        positions.append(surfaces.get_absolute_coordinates(s[i], p))
#                     print("(%f %f) (%f %f)" %(p[0], p[1], surfaces.get_absolute_coordinates(s[i], p)[0], surfaces.get_absolute_coordinates(s[i], p)[1]))
                if(len(positions) > 0):
                    if(act == 1):
                        # Pick case
                        # print(step_to_achieve.block.position)
                        block_to_pick = step_to_achieve.block.position
                        # print(block_to_pick)
                        block_to_pick = [surfaces.get_norm_coordinates(\
                                        step_to_achieve.get_stock_surface(),\
                                        p) for p in block_to_pick]
                        # print(block_to_pick)
                        block_to_pick = [surfaces.get_absolute_coordinates(\
                                        step_to_achieve.get_stock_surface(),\
                                        p) for p in block_to_pick]
                        # print(block_to_pick)
                        # print(positions)
                        dist = [distance_min_block_corner(p,block_to_pick) for p in positions]
                        n = 0
                        for d in dist:
                            if(d <= thresh):
                                n += 1
                        to_plot.append([step+offset, 100*float(n/len(dist))])
                    if(act == 2):
                        # print(step_to_achieve.block.position)
                        position_to_place = step_to_achieve.position_to_place
                        # print(block_to_pick)
                        position_to_place = [surfaces.get_norm_coordinates(\
                                        step_to_achieve.get_stock_surface(),\
                                        p) for p in position_to_place]
                        # print(block_to_pick)
                        position_to_place = [surfaces.get_absolute_coordinates(\
                                        step_to_achieve.get_stock_surface(),\
                                        p) for p in position_to_place]
                        # print(block_to_pick)
                        # print(positions)
                        dist = [distance_min_block_corner(p,position_to_place) for p in positions]
                        n = 0
                        # print(dist)
                        for d in dist:
                            if(d <= thresh):
                                n += 1
                        # print("%d %d %f" % (n, len(dist), float(n/len(dist))))
                        to_plot.append([step+offset, 100 * float(n/len(dist))])
                    else:
                        to_plot.append([step+offset, 0])

            ax.bar(*zip(*to_plot),width,label=actions.get_action_name(act))
        ax.legend()
    fig.savefig("output/png/%d_PLOT_FIXATION_DISTANCE_RATIO_%d.png" % (id, thresh))

def _PLOT_DISTANCE_OVER_TIME(id):
    print("_PLOT_DISTANCE_OVER_TIME %d" % id)

    for figId in figures.get_figures_id_list():
        nb_row = 3
        coord = [[0,0], [0,1], [0,2], \
                 [1,0], [1,1], [1,2], \
                 [2,0], [2,1], [2,2]]
        if(figId == 0):
            nb_row = 2
            coord = [[0,0], [0,1], [0,2], \
                 [1,0], [1,1], [1,2]]
        if(figId == 3):
            nb_row = 4
            coord = [[0,0], [0,1], [0,2], \
                 [1,0], [1,1], [1,2], \
                 [2,0], [2,1], [2,2], \
                 [3,0], [3,1], [3,2]]
        fig, axs = plt.subplots(nb_row, 3, figsize=(18, nb_row * 6))
        csvfile = ("../data/%d_%s_gazepoints.csv" % (id, figures.get_figure_name(figId)))
        gazepoints = GazePoints(csvfile)
#         width = float(1/(len(actions.get_actions_id_list())-1))
#         offset = -width*2
#         ax = axs[coord[figId][0], coord[figId][1]]
#         ax.set_title(figures.get_figure_name(figId).capitalize())
#         ax.set_xlabel('Step')
#         ax.set_ylabel('Distance (mm)')
#         ax.set_ylim(0,150)
        for step in range(1, figures.get_figure_n_steps(figId)+1): # Un graphe par étape, les deux actions dans le graphe
            ax = axs[coord[step-1][0], coord[step-1][1]]
            ax.set_title("%s - Step %d" % (figures.get_figure_name(figId).capitalize(), step))
            ax.set_xlabel('Timestamp (ms)')
            ax.set_ylabel('Distance (mm)')
            ax.set_ylim(0,300)
            for act in actions.get_actions_id_list():
                if(act == 0):
                    continue
                to_plot = []
                positions = []
                step_to_achieve = steps.get_step(figId, step)
                s = [gz.surface for gz in gazepoints.get_gazepoints(step, act)]
                x = [gz.x for gz in gazepoints.get_gazepoints(step, act)]
                y = [gz.y for gz in gazepoints.get_gazepoints(step, act)]
                tt = [gz.timestamp for gz in gazepoints.get_gazepoints(step, act)]
                if(len(s) > 0):
                    first_timestamp = min(tt)
                    positions = []
                    step_to_achieve = steps.get_step(figId, step)
                    t = []
                    for i in range(len(s)):
                        p = [x[i], y[i]]
                        if (act == 2 and s[i] == 2):
                            positions.append(surfaces.get_absolute_coordinates(s[i], p))
                            t.append(tt[i]-first_timestamp)
                        elif ((act == 1 or act == 0) and s[i] == step_to_achieve.get_stock_surface()):
                            positions.append(surfaces.get_absolute_coordinates(s[i], p))
                            t.append(tt[i]-first_timestamp)
                    if(act == 0):
                        block_to_pick = step_to_achieve.block.position
                        block_to_pick = [surfaces.get_norm_coordinates(\
                                         step_to_achieve.get_stock_surface(),\
                                         p) for p in block_to_pick]
                        block_to_pick = [surfaces.get_absolute_coordinates(\
                                          step_to_achieve.get_stock_surface(),\
                                          p) for p in block_to_pick]
                        dist = [distance_min_block_corner(p,block_to_pick) for p in positions]
                    if(act == 1):
                        block_to_pick = step_to_achieve.block.position
                        block_to_pick = [surfaces.get_norm_coordinates(\
                                         step_to_achieve.get_stock_surface(),\
                                         p) for p in block_to_pick]
                        block_to_pick = [surfaces.get_absolute_coordinates(\
                                          step_to_achieve.get_stock_surface(),\
                                          p) for p in block_to_pick]
                        dist = [distance_min_block_corner(p,block_to_pick) for p in positions]
                    if(act == 2):
                        position_to_place = step_to_achieve.position_to_place
                        position_to_place = [surfaces.get_norm_coordinates(\
                                            step_to_achieve.get_stock_surface(),\
                                            p) for p in position_to_place]
                        position_to_place = [surfaces.get_absolute_coordinates(\
                                            step_to_achieve.get_stock_surface(),\
                                            p) for p in position_to_place]
                        dist = [distance_min_block_corner(p,position_to_place) for p in positions]
                    to_plot = [[],[]]
                    for i in range(len(dist)):
                        to_plot[0].append(t[i])
                        to_plot[1].append(dist[i])
                    ax.scatter(to_plot[0], to_plot[1], label=actions.get_action_name(act))
                else:
                    ax.scatter([],[], label=actions.get_action_name(act))
            ax.legend()
        fig.savefig("output/png/%d_PLOT_DISTANCE_OVER_TIME_%s.png" % (id, figures.get_figure_name(figId).capitalize()))
