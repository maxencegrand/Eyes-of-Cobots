from conf.position import create_position, get_vertical, create_position_from_size
from conf.point import Point
from conf.block import Block
from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD
from conf.displays import get_surface, get_display

CSVFILE = "conf/csv/stock.csv"
KEY_BLOCK = "blockId"
KEY_COLOR = "colorId"
KEY_SHAPE = "shapeId"
KEY_X = "x"
KEY_Y = "y"
KEY_X_STOCK = "x_stock"
KEY_Y_STOCK = "y_stock"
KEY_WIDTH_STOCK = "width_stock"
KEY_HEIGHT_STOCK = "height_stock"
KEY_X_COLOR = "x_color"
KEY_Y_COLOR = "y_color"
KEY_WIDTH_COLOR = "width_color"
KEY_HEIGHT_COLOR = "height_color"
KEY_X_SHAPE = "x_shape"
KEY_Y_SHAPE = "y_shape"
KEY_WIDTH_SHAPE = "width_shape"
KEY_HEIGHT_SHAPE = "height_shape"

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
                    x = _GET(blocks2, color, KEY_X, keyId=KEY_COLOR)
                    y = _GET(blocks2, color, KEY_Y, keyId=KEY_COLOR)
                    block = Block(id, color,shape)
                    point = Point(x,y)
                    position = create_position(block, point, get_vertical())
                    position = get_display(1).get_real_position_from_absolute(\
                                                                    position)
                    position_stock = create_position_from_size(\
                    Point(_GET(blocks2, color, KEY_X_STOCK, keyId=KEY_COLOR),\
                            _GET(blocks2, color, KEY_Y_STOCK, keyId=KEY_COLOR)),
                    _GET(blocks2, color, KEY_WIDTH_STOCK, keyId=KEY_COLOR),\
                    _GET(blocks2, color, KEY_HEIGHT_STOCK, keyId=KEY_COLOR)
                    )
                    position_color = create_position_from_size(\
                    Point(_GET(blocks2, color, KEY_X_COLOR, keyId=KEY_COLOR),\
                            _GET(blocks2, color, KEY_Y_COLOR, keyId=KEY_COLOR)),
                    _GET(blocks2, color, KEY_WIDTH_COLOR, keyId=KEY_COLOR),\
                    _GET(blocks2, color, KEY_HEIGHT_COLOR, keyId=KEY_COLOR)
                    )
                    position_shape = create_position_from_size(\
                    Point(_GET(blocks2, color, KEY_X_SHAPE, keyId=KEY_COLOR),\
                            _GET(blocks2, color, KEY_Y_SHAPE, keyId=KEY_COLOR)),
                    _GET(blocks2, color, KEY_WIDTH_SHAPE, keyId=KEY_COLOR),\
                    _GET(blocks2, color, KEY_HEIGHT_SHAPE, keyId=KEY_COLOR)
                    )
                    self.blocks[id][shape][color] = {"block":block,\
                                                "position":position,\
                                                "position_stock":position_stock,\
                                                "position_color":position_color,\
                                                "position_shape":position_shape}

    def __str__(self):
        str = ""
        for id in [0,1,2]:
            for shape in [0,1]:
                for color in [0,1,2,3]:
                    str += (f"{self.get_block(id,shape,color)} ")
                    str += (f"at {self.get_position(id,shape,color)}\n")
        return str

    def get(self, id, shape, color, key):
        return self.blocks[id][shape][color][key]

    def get_block(self, id, shape, color):
        return self.get(id,shape,color,"block")

    def get_position(self, id, shape, color):
        return self.get(id,shape,color,"position")

    def get_position_stock(self, id, shape, color):
        return self.get(id,shape,color,"position_stock")

    def get_position_color(self, id, shape, color):
        return self.get(id,shape,color,"position_color")

    def get_position_shape(self, id, shape, color):
        return self.get(id,shape,color,"position_shape")
