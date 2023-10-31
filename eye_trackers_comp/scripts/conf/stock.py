from conf.position import create_position, get_vertical
from conf.point import Point
from conf.block import Block
from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD

CSVFILE = "conf/csv/stock.csv"
KEY_BLOCK = "blockId"
KEY_SURFACE = "surfaceId"
KEY_COLOR = "colorId"
KEY_SHAPE = "shapeId"
KEY_X = "x"
KEY_Y = "y"

class Stock:
    def __init__(self):
        table = _LOAD(CSVFILE)
        # (id x shape x color) -> (block x position)
        self.blocks = {}
        for id in [0,1,2]:
            self.blocks[id] = {}
            blocks_ = _GET_ALL(table, id, KEY_BLOCK)
            for shape in [0,1]:
                self.blocks[id][shape] = {}
                blocks2 = _GET_ALL(blocks_, shape, KEY_SHAPE)
                for color in [0,1,2,3]:
                    surface = _GET(blocks2, color, KEY_SURFACE, keyId=KEY_COLOR)
                    x = _GET(blocks2, color, KEY_X, keyId=KEY_COLOR)
                    y = _GET(blocks2, color, KEY_Y, keyId=KEY_COLOR)
                    block = Block(color,shape)
                    point = Point(x,y)
                    position = \
                        create_position(block, point, get_vertical(), surface)
                    self.blocks[id][shape][color] = {"block":block,\
                                                        "position":position}

    def __str__(self):
        str = ""
        for id in [0,1,2]:
            for shape in [0,1]:
                for color in [0,1,2,3]:
                    str += (f"{self.get_block(id,shape,color)}")
                    str += (f"at {self.get_position(id,shape,color)}\n")
        return str

    def get(self, id, shape, color, key):
        return self.blocks[id][shape][color][key]

    def get_block(self, id, shape, color):
        return self.get(id,shape,color,"block")

    def get_position(self, id, shape, color):
        return self.get(id,shape,color,"position")
