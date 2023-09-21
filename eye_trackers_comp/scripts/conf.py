import constants as cst
from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES
from utils import centroid

class Position:
    def __init__(self, top_left, top_right, bottom_right, bottom_left):
        self.top_right = top_right
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left

    def center(self):
        return centroid([self.top_left, self.top_right,\
                            self.bottom_right, self.bottom_left])

class Block:
    def __init__(self, color, shape, position, surface):
        self.color = color
        self.shape = shape
        self.position = position
        self.surface = surface

    def center(self):
        return self.position.center()


class Users:
    # LOAD USERS DATASET
    def __init__(self,pretest=False):
        if pretest:
            self.table = _LOAD(cst._USERS_CSV_PRETEST)
        else:
            self.table = _LOAD(cst._USERS_CSV)

    # Return all users id
    def get_users_id_list(self):
        return self.table[cst._KEY_USER_ID].tolist()

    #Return
    def get_records(self, id):
        return _GET(self.table, id, cst._KEY_USER_RECORD_REP, keyId=cst._KEY_USER_ID)

    def get_score(self,id):
        return float( _GET(self.table, id, cst._KEY_USER_SCORE_1, keyId=cst._KEY_USER_ID) +
                             _GET(self.table, id, cst._KEY_USER_SCORE_2))

    def get_setup(self, id):
        return _GET(self.table,id, cst._KEY_USER_SETUP_ID, keyId=cst._KEY_USER_ID)

    def get_position(self, id):
        return _GET(self.table,id, cst._KEY_USER_POSITION_ID, keyId=cst._KEY_USER_ID)

    def get_order(self, id):
        return _GET(self.table,id, cst._KEY_USER_ORDER_ID, keyId=cst._KEY_USER_ID)

    #
    def print_user_info(self,id):
        print()
        print("User ID: %d" % int(id))
        print("\t%s" % self.get_records(id))
        print("\tScore : %f" % self.get_score(id))
        print("\tPosition ID : %d" % self.get_position(id))
        print("\tSetup ID : %d" % self.get_setup(id))
        print("\tOrder ID : %d" % self.get_order(id))

    def print_all_users_info(self):
        for id in self.get_users_id_list():
            self.print_user_info(id)

class Actions:
    def __init__(self):
        self.table = _LOAD(cst._ACTIONS_CSV)

    def get_action_name(self, id):
        return  _GET(self.table, id, cst._KEY_ACTION_NAME)

    def get_actions_id_list(self):
        return _TOLIST(self.table, cst._KEY_ACTION_ID)

class Figures:
    def __init__(self):
        self.table = _LOAD(cst._FIGURES_CSV)

    def get_figure_name(self, id):
        return  _GET(self.table, id, cst._KEY_FIGURE_NAME)

    def get_figure_n_steps(self, id):
        return  _GET(self.table, id, cst._KEY_FIGURE_STEPS)

    def get_figures_id_list(self):
        return _TOLIST(self.table, cst._KEY_FIGURE_ID)

class Surface:
    def __init__(self):
        self.table = _LOAD(cst._SURFACES_CSV)

    def get_surfaces_id_list(self):
        return _TOLIST(self.table, cst._KEY_SURFACE_ID)

    def get_surface_name(self, id):
        res = _GET(table = self.table, id = id, key = cst._KEY_SURFACE_NAME, keyId = cst._KEY_SURFACE_ID)
        return res

    def get_norm_coordinates(self, id, coordinate):
        return [float(coordinate[0]/_GET(self.table, id, cst._KEY_SURFACE_WIDTH)),\
                float(coordinate[1]/_GET(self.table, id, cst._KEY_SURFACE_HEIGHT))]

    def get_absolute_coordinates(self, id, coordinate):
        return [float(coordinate[0])*_GET(self.table, id, cst._KEY_SURFACE_WIDTH_MM),\
                float(coordinate[1])*_GET(self.table, id, cst._KEY_SURFACE_HEIGHT_MM)]

class Point:
    def __init__(self, x, y, surface, conf, markers, time):
        self.x = x
        self.y = y
        self.surface = surface
        self.conf = conf
        self.markers = markers
        self.timestamp = time

class GazePoints:
    def __init__(self, csvfile):
        self.table = _LOAD(csvfile)

    def get_gazepoints(self, step, action):
        points = []
        s = _GET_ALL_VALUES(_GET_ALL(self.table, action, keyId=cst._KEY_GAZEPOINTS_ACTION),\
                step, cst._KEY_GAZEPOINTS_SURFACE, keyId=cst._KEY_GAZEPOINTS_STEP)
        time = _GET_ALL_VALUES(_GET_ALL(self.table, action, keyId=cst._KEY_GAZEPOINTS_ACTION),\
                step, cst._KEY_GAZEPOINTS_TIMESTAMPS, keyId=cst._KEY_GAZEPOINTS_STEP)
        x = _GET_ALL_VALUES(_GET_ALL(self.table, action, keyId=cst._KEY_GAZEPOINTS_ACTION),\
                step, cst._KEY_GAZEPOINTS_X, keyId=cst._KEY_GAZEPOINTS_STEP)
        y = _GET_ALL_VALUES(_GET_ALL(self.table, action, keyId=cst._KEY_GAZEPOINTS_ACTION),\
                step, cst._KEY_GAZEPOINTS_Y, keyId=cst._KEY_GAZEPOINTS_STEP)
        conf = _GET_ALL_VALUES(_GET_ALL(self.table, action, keyId=cst._KEY_GAZEPOINTS_ACTION),\
                step, cst._KEY_GAZEPOINTS_CONFIDENCE, keyId=cst._KEY_GAZEPOINTS_STEP)
        markers = _GET_ALL_VALUES(_GET_ALL(self.table, action, keyId=cst._KEY_GAZEPOINTS_ACTION),\
                step, cst._KEY_GAZEPOINTS_MARKERS, keyId=cst._KEY_GAZEPOINTS_STEP)
        for i in range(len(x)):
            points.append(Point(x[i], y[i], s[i], conf[i], markers[i], time[i]))
        return points

class Fixation:
    def __init__(self, x, y, surface, duration, disp, timestamp):
        self.x = x
        self.y = y
        self.surface = surface
        self.disp = disp
        self.duration = duration
        self.timestamp = timestamp

class Fixations:
    def __init__(self, csvfile):
        self.table = _LOAD(csvfile)

    def get_fixations(self, step, action):
        fixations = []
        s = _GET_ALL_VALUES(_GET_ALL(self.table, action, keyId=cst._KEY_FIXATION_ACTION),\
                step, cst._KEY_FIXATION_SURFACE, keyId=cst._KEY_FIXATION_STEP)
        d = _GET_ALL_VALUES(_GET_ALL(self.table, action, keyId=cst._KEY_FIXATION_ACTION),\
                step, cst._KEY_FIXATION_DURATION, keyId=cst._KEY_FIXATION_STEP)
        x = _GET_ALL_VALUES(_GET_ALL(self.table, action, keyId=cst._KEY_FIXATION_ACTION),\
                step, cst._KEY_FIXATION_X, keyId=cst._KEY_FIXATION_STEP)
        y = _GET_ALL_VALUES(_GET_ALL(self.table, action, keyId=cst._KEY_FIXATION_ACTION),\
                step, cst._KEY_FIXATION_Y, keyId=cst._KEY_FIXATION_STEP)
        disp = _GET_ALL_VALUES(_GET_ALL(self.table, action, keyId=cst._KEY_FIXATION_ACTION),\
                step, cst._KEY_FIXATION_DISP, keyId=cst._KEY_FIXATION_STEP)
        time = _GET_ALL_VALUES(_GET_ALL(self.table, action, keyId=cst._KEY_FIXATION_ACTION),\
                step, cst._KEY_FIXATION_TIMESTAMPS, keyId=cst._KEY_FIXATION_STEP)
        for i in range(len(s)):
            fixations.append(Fixation(x[i], y[i], s[i], d[i], disp[i], time[i]))
        return fixations

class Stock:
    def __init__(self):
        self.table = _LOAD(cst._STOCK_CSV)

    def get_block(self, block, color, shape):
        tmp = _GET_ALL(self.table, block, cst._KEY_STOCK_BLOCK_ID)
        tmp = _GET_ALL(tmp, color, cst._KEY_STOCK_COLOR_ID)
        surface = _GET(tmp, shape, cst._KEY_STOCK_SURFACE_ID, keyId=cst._KEY_STOCK_SHAPE_ID)
        position = [
            [_GET(tmp, shape, cst._KEY_STOCK_X1, keyId=cst._KEY_STOCK_SHAPE_ID),_GET(tmp, shape, cst._KEY_STOCK_Y1, keyId=cst._KEY_STOCK_SHAPE_ID)],\
            [_GET(tmp, shape, cst._KEY_STOCK_X2, keyId=cst._KEY_STOCK_SHAPE_ID),_GET(tmp, shape, cst._KEY_STOCK_Y2, keyId=cst._KEY_STOCK_SHAPE_ID)],\
            [_GET(tmp, shape, cst._KEY_STOCK_X3, keyId=cst._KEY_STOCK_SHAPE_ID),_GET(tmp, shape, cst._KEY_STOCK_Y3, keyId=cst._KEY_STOCK_SHAPE_ID)],\
            [_GET(tmp, shape, cst._KEY_STOCK_X4, keyId=cst._KEY_STOCK_SHAPE_ID),_GET(tmp, shape, cst._KEY_STOCK_Y4, keyId=cst._KEY_STOCK_SHAPE_ID)]
        ]

        return Block(color, shape, position, surface)

    def get_block_list(self):
        ids = _TOLIST(self.table, cst._KEY_SURFACE_ID)
        return ids

class Step:
    def __init__(self, block, position_to_place):
        self.block = block
        self.position_to_place = position_to_place

    def get_stock_surface(self):
        return self.block.surface

class Steps:
    def __init__(self):
        self.table = _LOAD(cst._STEP_CSV)
        self.stock = Stock()

    def get_step(self, figId, stepId):
        tmp = _GET_ALL(self.table, figId, cst._KEY_STEP_FIGURE)
        block = self.stock.get_block(_GET(tmp, stepId, cst._KEY_STEP_BLOCK, keyId=cst._KEY_STEP_STEP),\
                    _GET(tmp, stepId, cst._KEY_STEP_COLOR, keyId=cst._KEY_STEP_STEP),\
                    _GET(tmp, stepId, cst._KEY_STEP_SHAPE, keyId=cst._KEY_STEP_STEP))
        position = [
            [_GET(tmp, stepId, cst._KEY_STEP_X1, keyId=cst._KEY_STEP_STEP),_GET(tmp, stepId, cst._KEY_STEP_Y1, keyId=cst._KEY_STEP_STEP)],\
            [_GET(tmp, stepId, cst._KEY_STEP_X2, keyId=cst._KEY_STEP_STEP),_GET(tmp, stepId, cst._KEY_STEP_Y2, keyId=cst._KEY_STEP_STEP)],\
            [_GET(tmp, stepId, cst._KEY_STEP_X3, keyId=cst._KEY_STEP_STEP),_GET(tmp, stepId, cst._KEY_STEP_Y3, keyId=cst._KEY_STEP_STEP)],\
            [_GET(tmp, stepId, cst._KEY_STEP_X4, keyId=cst._KEY_STEP_STEP),_GET(tmp, stepId, cst._KEY_STEP_Y4, keyId=cst._KEY_STEP_STEP)],\
        ]
        return Step(block, position)

# users=Users()
# print(users.table)
# print(users.get_users_id_list())
# print(users.print_all_users_info())
# actions=Actions()
# print(actions.table)
# print(actions.get_actions_id_list())
# for actId in actions.get_actions_id_list():
#     print("ID %d -- %s" % (actId, actions.get_action_name(actId)))
# figures=Figures()
# print(figures.table)
# print(figures.get_figures_id_list())
# for figId in figures.get_figures_id_list():
#     print("ID %d -- %s %d" % (figId, figures.get_figure_name(figId), figures.get_figure_n_steps(figId)))
