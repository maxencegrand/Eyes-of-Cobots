import csv

def extract(id, figure, events):
    data = []
    for i in range(len(events.index)-1):
        idx_current_step = events.index[i]
        idx_next_step = events.index[i+1]
        begin_ts = events.at[idx_current_step,"timestamp"]
        end_ts = events.at[idx_next_step,"timestamp"]
        data.append([events.at[idx_current_step,"stepId"],
            begin_ts,\
            (end_ts-begin_ts)])
    csvfile = ("../data/%s/steps_duration_%s.csv" % (id,figure))
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["stepId", "timestamp", "duration"])
        for row in data:
            spamwriter.writerow(row)
