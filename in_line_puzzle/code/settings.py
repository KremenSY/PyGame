import os

BASE_DIR=os.path.dirname(os.path.dirname(__file__))

# MAP SETTINGS
# 0-no tile render, tiles of type 1, 2, 3 can be moved here
# 1,2,3-movable tiles
# 4-this tile can't be moved
WIN_MAP=[
        [1,4,2,4,3],
        [1,0,2,0,3],
        [1,4,2,4,3],
        [1,0,2,0,3],
        [1,4,2,4,3]
        ]
test_map=[
        [1,4,2,4,3],
        [0,1,2,0,3],
        [1,4,2,4,3],
        [1,0,2,0,3],
        [1,4,2,4,3]
        ]

# GAME SETTINGS
RES = WIDTH, HEIGHT = 600, 600
TILE_SIZE=64
FPS = 0
MARGIN=HORIZONTAL_MARGIN, VERTICAL_MARGIN= (WIDTH-len(WIN_MAP)*TILE_SIZE)//2, (HEIGHT-len(WIN_MAP[0])*TILE_SIZE)//2


