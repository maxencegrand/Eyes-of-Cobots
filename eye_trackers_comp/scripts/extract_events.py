from conf.actions import get_name
from conf.event import create_event
from conf.step import get_all_step_events, get_event
from conf.figures import get_figure_id
import pandas as pd

KEY_TIMESTAMP = "timestamp"
KEY_ACTION = "actionId"
def extract(id, figure, steps):
    #read event data
    csvfile = ("../data/%s/event_%s.csv" % (id,figure))
    df_event = pd.DataFrame(data=pd.read_csv (csvfile))
    step_events = get_all_step_events(get_figure_id(figure), steps)
    events = []
    for idx in df_event.index:
        timestamp = df_event.at[idx, KEY_TIMESTAMP]
        action = df_event.at[idx, KEY_ACTION]
        event = get_event(timestamp, get_name(action), step_events)
        events.append(event)
    return events
