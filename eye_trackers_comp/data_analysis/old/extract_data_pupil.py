import pandas as pd
import csv
import sys, getopt
from conf import Users, Figures
SURFACE = {
    0:"Screen",\
    1:"Right_Stock",\
    2:"Assemly_Zone",\
    3:"Left_Stock"
}

def extract_gaze_points(id, figure, df_actions):
    print("\tExtract Gaze Points")
    df_surfaces = []
    df_surf_positions = []
    idx_surface = []
    gazepoints = []
    for s in SURFACE.keys():
        csvfile = ("../data/recordings/%s/%s/surfaces/gaze_positions_on_surface_%s.csv" % (id,figure,SURFACE[s]))
        data = pd.read_csv (csvfile)
        df_surfaces.append( pd.DataFrame(data=data))
        idx_surface.append(0)
        csvfile = ("../data/recordings/%s/%s/surfaces/surf_positions_%s.csv" % (id,figure,SURFACE[s]))
        data = pd.read_csv (csvfile)
        df_surf_positions.append( pd.DataFrame(data=data))


    for idx in df_actions.index:
        begin = df_actions.at[idx,"begin"]
        end = df_actions.at[idx,"end"]
        # print("%d %d %d" % (idx,begin,end))
        for s in SURFACE.keys():
            df = df_surfaces[s]
            dfs = df_surf_positions[s]
            i = idx_surface[s]
            # print("\t%d %d" % (i, df.at[i,"world_index"]))
            # df.at[i,"world_index"]
            while i < df.shape[0] and df.at[i,"world_index"] <= end:
                if(df.at[i,"world_index"] >= begin):
                    if(df.at[i,"on_surf"]):
                        x = dfs.loc[dfs["world_index"] == df.at[i,"world_index"]]
                        # print([df.at[i,"gaze_timestamp"]*1000,\
                        #                         df_actions.at[idx,"stepId"],\
                        #                         df_actions.at[idx,"actionId"],\
                        #                         s,\
                        #                         df.at[i,"x_norm"],\
                        #                         df.at[i,"y_norm"],\
                        #                         df.at[i,"confidence"],\
                        #                         float(x.at[x.index[0], "num_detected_markers"] / x.at[x.index[0], "num_definition_markers"])])
                        gazepoints.append([df.at[i,"gaze_timestamp"]*1000,\
                                                df_actions.at[idx,"stepId"],\
                                                df_actions.at[idx,"actionId"],\
                                                s,\
                                                df.at[i,"x_norm"],\
                                                df.at[i,"y_norm"],\
                                                df.at[i,"confidence"],\
                                                float(x.at[x.index[0], "num_detected_markers"] / x.at[x.index[0], "num_definition_markers"])])
                i += 1
            idx_surface[s] = i

    csvfile = ("../data/%s_%s_gazepoints.csv" % (id,figure))
    # print(csvfile)
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["timestamp","stepId", "actionId", "surfaceId", "x", "y", "confidence", "markers"])
        for g in gazepoints:
            spamwriter.writerow(g)

def extract_fixations(id, figure, df_actions):
    print("\tExtract Pupil Fixations")
    df_surfaces = []
    idx_surface = []
    gazepoints = []
    for s in SURFACE.keys():
        csvfile = ("../data/recordings/%s/%s/surfaces/fixations_on_surface_%s.csv" % (id,figure,SURFACE[s]))
        data = pd.read_csv (csvfile)
        df_surfaces.append( pd.DataFrame(data=data))
        idx_surface.append(0)

    for idx in df_actions.index:
        begin = df_actions.at[idx,"begin"]
        end = df_actions.at[idx,"end"]
        # print("%d %d %d" % (idx,begin,end))
        for s in SURFACE.keys():
            df = df_surfaces[s]
            i = idx_surface[s]
            # print("\t%d %d %d %d" % (i, df.at[i,"world_index"], begin, end))
            # print(SURFACE[s])
            # print(df.at[i,"world_index"])
            # if(i >= df.shape[0]):
            #     continue
            while i < df.shape[0] and df.at[i,"world_index"] <= end:
                # print("test1")
                if(df.at[i,"world_index"] >= begin):
                    # print("test2")
                    if(df.at[i,"on_surf"]):
                        # print("test3")
                        gazepoints.append([df.at[i,"start_timestamp"]*1000,\
                                                df_actions.at[idx,"stepId"],\
                                                df_actions.at[idx,"actionId"],\
                                                s,\
                                                df.at[i,"norm_pos_x"],\
                                                df.at[i,"norm_pos_y"],\
                                                df.at[i,"duration"],\
                                                df.at[i,"dispersion"]])
                #     else:
                #         print("\t%d %d %d %d %d" % (i, df.at[i,"world_index"], begin, end, df.shape[0]))
                # else:
                #     print("\t%d %d %d %d %d" % (i, df.at[i,"world_index"], begin, end, df.shape[0]))
                i += 1
            idx_surface[s] = i

    csvfile = ("../data/%s_%s_fixations.csv" % (id,figure))
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["timestamp","stepId", "actionId", "surfaceId", "x", "y", "duration", "dispertion"])
        for g in gazepoints:
            spamwriter.writerow(g)

def extract_action_durations(id,figure,df_actions):
    print("\tExtract Action Duration")
    csvfile = ("../data/recordings/%s/%s/world_timestamps.csv" % (id,figure))
    data = pd.read_csv (csvfile)
    df = pd.DataFrame(data=data)
    ts = []
    for idx in df_actions.index:
        begin = df_actions.at[idx,"begin"]
        end = df_actions.at[idx,"end"]
        begin_ts = df.at[begin,"# timestamps [seconds]"]*1000
        end_ts = df.at[end,"# timestamps [seconds]"]*1000
        ts.append([df_actions.at[idx,"stepId"],\
            df_actions.at[idx,"actionId"],\
            begin_ts,\
            (end_ts-begin_ts)])
    csvfile = ("../data/%s_%s_actions.csv" % (id,figure))
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["stepId", "actionId", "timestamp", "duration"])
        for g in ts:
            spamwriter.writerow(g)

def extract_surface_time(id, figure, df_actions):
    table = pd.DataFrame({"idx":[], "id":[]})
    print("\tExtract Surface Time")
    df_surfaces = []
    idx_surface = []
    gazepoints = []
    for s in SURFACE.keys():
        csvfile = ("../data/recordings/%s/%s/surfaces/fixations_on_surface_%s.csv" % (id,figure,SURFACE[s]))
        data = pd.read_csv (csvfile)
        df_surfaces.append( pd.DataFrame(data=data))
        idx_surface.append(0)
    csvfile = ("../data/recordings/%s/%s/world_timestamps.csv" % (id,figure))
    data = pd.read_csv (csvfile)
    world = pd.DataFrame(data=data)
    nb_frame = world.shape[0]-1
    for frame in range(world.shape[0]):
        no_surf = True
        for s in SURFACE.keys():
            request = df_surfaces[s].loc[df_surfaces[s]["world_index"] == frame]
            if(len(request.index) > 0):
                for idxRequest in range(len(request.index)):
                    if(df_surfaces[s].at[request.index[idxRequest], "on_surf"]):
                        no_surf = False
                        table.loc[len(table.index)] = [frame, s]
                        break
        if(no_surf):
            table.loc[len(table.index)] = [frame, -1]
    interval = {-1:[]}
    for s in SURFACE.keys():
        interval[s]=[]
    for idx in table.index:
        frame = table.loc[idx]["idx"]
        surf = table.loc[idx]["id"]
        if(len(interval[surf]) == 0):
            interval[surf].append([frame, frame])
        # else:
        #     print(interval[surf][len(interval[surf])-1] )
        elif (interval[surf][len(interval[surf])-1][1]+1 < frame):
            interval[surf].append([frame, frame])
        elif (interval[surf][len(interval[surf])-1][1]+1 == frame):
            interval[surf][len(interval[surf])-1][1] += 1
    idx_surface = {}
    for k in interval.keys():
        idx_surface[k] = 0
    table = pd.DataFrame({"id":[], "begin":[], "end":[]})
    again = True
    while (again):
        again = False
        min_surf = -1
        for k in interval.keys():
            if(idx_surface[k] < len(interval[k])):
                again = True
                if(idx_surface[min_surf] < len(interval[min_surf])):
                    if(interval[k][idx_surface[k]][0] < interval[min_surf][idx_surface[min_surf]][0]):
                        min_surf = k
                else:
                    min_surf = k
        if(again):
            frames = interval[min_surf][idx_surface[min_surf]]
            if(frames[0] < frames[1]):
                table.loc[len(table.index)] = [min_surf, frames[0], frames[1]]
            idx_surface[min_surf] += 1
    current = 0
    table2 = pd.DataFrame({"stepId":[], "actionId":[], "surfaceId":[], "timestamp":[], "duration":[]})
    for idx in df_actions.index:
        begin = df_actions.at[idx,"begin"]
        end = df_actions.at[idx,"end"]
        while(current < len(table.index)):
            begin_surf = table.loc[current]["begin"]
            end_surf = table.loc[current]["end"]
            if(begin_surf > end):
                break
            if(begin_surf >= begin and begin_surf < end):
                if(end_surf < end):
                    step = df_actions.at[idx,"stepId"]
                    act = df_actions.at[idx,"actionId"]
                    surf = table.loc[current]["id"]
                    timestamp = world.at[begin_surf, "# timestamps [seconds]"]*1000
                    duration = world.at[end_surf, "# timestamps [seconds]"]*1000-timestamp
                    table2.loc[len(table2.index)] = [step, act, surf, timestamp, duration]
                if(end_surf >= end):
                    step = df_actions.at[idx,"stepId"]
                    act = df_actions.at[idx,"actionId"]
                    surf = table.loc[current]["id"]
                    timestamp = world.at[begin_surf, "# timestamps [seconds]"]*1000
                    duration = world.at[end, "# timestamps [seconds]"]*1000-timestamp
                    table2.loc[len(table2.index)] = [step, act, surf, timestamp, duration]
            if(begin_surf < begin and end_surf >= begin):
                if(end_surf < end):
                    step = df_actions.at[idx,"stepId"]
                    act = df_actions.at[idx,"actionId"]
                    surf = table.loc[current]["id"]
                    timestamp = world.at[begin, "# timestamps [seconds]"]*1000
                    duration = world.at[end_surf, "# timestamps [seconds]"]*1000-timestamp
                    table2.loc[len(table2.index)] = [step, act, surf, timestamp, duration]
                if(end_surf >= end):
                    step = df_actions.at[idx,"stepId"]
                    act = df_actions.at[idx,"actionId"]
                    surf = table.loc[current]["id"]
                    timestamp = world.at[begin, "# timestamps [seconds]"]*1000
                    duration = world.at[end, "# timestamps [seconds]"]*1000-timestamp
                    table2.loc[len(table2.index)] = [step, act, surf, timestamp, duration]
            current +=1
    csvfile = ("../data/%s_%s_surfaces_duration.csv" % (id,figure))
    table2.to_csv(csvfile, index=False)

def extract(id, figure):
    csvfile = ("../data/%s_%s.csv" % (id,figure))
    data = pd.read_csv (csvfile)
    df_actions = pd.DataFrame(data=data)
    extract_fixations(id,figure,df_actions)
    extract_gaze_points(id,figure,df_actions)
    extract_action_durations(id,figure,df_actions)
    extract_surface_time(id,figure,df_actions)

def main(argv):
    print("Extracting data ...")
    users = Users()
    figures = Figures()
    for id in users.get_users_id_list():
        users.print_user_info(id)
        for figId in figures.get_figures_id_list():
            print("Extract %s"%figures.get_figure_name(figId))
            extract(id, figures.get_figure_name(figId))
    print("Done")


if __name__ == "__main__":
   main(sys.argv[1:])
