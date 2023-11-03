def get_points(begin, end, points):
    res = []
    for p in points:
        if(p.timestamp <= end and p.timestamp >= begin):
            res.append(p)
    return res

def extract(id, figure, steps, events):
    return
