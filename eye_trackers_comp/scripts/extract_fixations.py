import pandas as pd
import csv
import sys, getopt

SURFACE = {
    0:"Screen",\
    1:"Right_Stock",\
    2:"Assemly_Zone",\
    3:"Left_Stock"
}

def main(argv):
    id = ""
    figure=""
    opts, args = getopt.getopt(argv,"h:i:f:")
    for opt, arg in opts:
        if opt == '-h':
            print ('segmentation.py -id <subject identifier> -figure <figure\'s name>')
            sys.exit()
        elif opt in ("-i"):
            id = arg
        elif opt in ("-f"):
            figure = arg
    csvfile = ("data/%s_%s.csv" % (id,figure))
    data = pd.read_csv (csvfile)
    df_actions = pd.DataFrame(data=data)
    df_surfaces = []
    idx_surface = []
    gazepoints = []
    for s in SURFACE.keys():
        csvfile = ("data/%s/%s/surfaces/fixations_on_surface_%s.csv" % (id,figure,SURFACE[s]))
        data = pd.read_csv (csvfile)
        df_surfaces.append( pd.DataFrame(data=data))
        idx_surface.append(0)

    for idx in df_actions.index:
        begin = df_actions.at[idx,"Begin"]
        end = df_actions.at[idx,"End"]
        # print("%d %d %d" % (idx,begin,end))
        for s in SURFACE.keys():
            df = df_surfaces[s]
            i = idx_surface[s]
            # print("\t%d %d" % (i, df.at[i,"world_index"]))
            while df.at[i,"world_index"] <= end:
                if(df.at[i,"world_index"] >= begin):
                    if(df.at[i,"on_surf"]):
                        gazepoints.append([df.at[i,"start_timestamp"]*1000,\
                                                df_actions.at[idx,"Step id"],\
                                                df_actions.at[idx,"Action id"],\
                                                s,\
                                                df.at[i,"norm_pos_x"],\
                                                df.at[i,"norm_pos_y"],\
                                                df.at[i,"duration"],\
                                                df.at[i,"dispersion"]])
                i += 1
            idx_surface[s] = i

    csvfile = ("data/%s_%s_fixations.csv" % (id,figure))
    print(csvfile)
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Timestamp","Step id", "Action id", "Surface id", "x", "y", "Duration", "Dispertion"])
        for g in gazepoints:
            spamwriter.writerow(g)
if __name__ == "__main__":
   main(sys.argv[1:])
