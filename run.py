from GUI import Console
from config import *
import os

try:
    os.makedirs("maze")
except FileExistsError:
    pass

Console(ROW, COLUMN, CELL_SIZE)
