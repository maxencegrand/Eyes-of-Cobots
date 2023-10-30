from position import Position
from block import Block
from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD

CSVFILE = "csv/stock.csv"
KEY_BLOCK = "blockId"
KEY_SURFACE = "surfaceId"
KEY_COLOR = "colorId"
KEY_SHAPE = "shapeId"
KEY_X = "x"
KEY_y = "y"

class Stock:
    def __init__(self):
        table = _LOAD(CSVFILE)
        self.blocks = {}

s = Stock()
print(s.blocks)
