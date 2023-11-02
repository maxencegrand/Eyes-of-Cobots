import csv
from conf.step import Step, write_csv

def extract(id, figure, events):
    data = []
    for i in range(len(events.index)-1):
        idx_current_step = events.index[i]
        idx_next_step = events.index[i+1]
        begin_ts = events.at[idx_current_step,"timestamp"]
        end_ts = events.at[idx_next_step,"timestamp"]
        step = Step(events.at[idx_current_step,"stepId"], begin_ts, end_ts)
        data.append(step)

    csvfile = ("../data/%s/steps_duration_%s.csv" % (id,figure))
    write_csv(data, csvfile)
