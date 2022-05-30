import tkinter.ttk
from tkinter import *
from SearchAlgo import AStar
from tkinter import messagebox
from PIL import Image, ImageColor
from config import COLOR
from MazeAlgo import BackTracking


class Cell:

    def __init__(self, master, x, y, size):
        self.master = master
        self.x, self.y, self.size = x, y, size
        self.fill = False
        x_1 = self.x * self.size
        y_1 = self.y * self.size
        x_2 = x_1 + self.size
        y_2 = y_1 + self.size

        self.num = self.master.create_rectangle(x_1, y_1, x_2, y_2, fill=COLOR["empty"], outline=COLOR["border"])

    def switch(self):
        """
        Switch the state of the cell
        :return: None
        """
        self.fill = not self.fill
        return self.fill


class CellGrid(Canvas):
    def __init__(self, master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        """
        Initialize the 2D grid
        :param master: The window you wish to pack
        :param rowNumber: Numbers of row
        :param columnNumber: Numbers of column
        :param cellSize: The size for the grid
        """
        Canvas.__init__(self, master, width=cellSize * columnNumber, height=cellSize * rowNumber, *args, **kwargs)
        self.cellSize, self.__rowNum, self.__colNum = cellSize, rowNumber, columnNumber
        self.grid, self.map, self.path, self.expanded = [], [], [], []
        self.cost, self.cnt = 0, 0
        for r in range(rowNumber):
            self.grid.append(
                [Cell(self, c, r, cellSize) for c in range(columnNumber)])
            self.map.append(
                [1 for c in range(columnNumber)])

        self.target, self.source = (), ()
        self.maze = False

        self.bind("<Button-1>", lambda event: self.__AddTargetSource(event, COLOR["block"]))
        self.bind("<Button-2>", lambda event: self.__AddTargetSource(event, COLOR["source"]))
        self.bind("<Button-3>", lambda event: self.__AddTargetSource(event, COLOR["target"]))
        self.bind("<B1-Motion>", lambda event: self.__AddTargetSource(event,COLOR["block"]))
        self.bind("<MouseWheel>",  self.__zoom)

        # self.bind("<Motion>", lambda event:  print(event.x, event.y))

    def __Coords(self, num):
        """
        Get the actual row and column for the small rectangle
        :param num: The id of rectangle respect to the 2D grid
        :return: Index of row and column
        """
        r = num[0] // self.__colNum if num[0] % self.__colNum else (num[0] // self.__colNum) - 1
        c = (num[0] - r  * self.__colNum) - 1
        return r, c if c != -1 else self.__colNum - 1

    def __AddTargetSource(self, event, color):
        """
        Add the blocks, source or target
        :param event: Tkinter event
        :param color: Type of blocks you wish to put
        :return: None
        """
        num = event.widget.find_closest(event.x, event.y)
        row, column = self.__Coords(num)
        cell = self.grid[row][column]

        if cell.switch():
            self.itemconfig(num, fill=color, outline=color if self.maze else COLOR["border"])
            if color == COLOR["block"]:
                self.map[row][column] = int(not self.map[row][column])
            elif color == COLOR["source"]:
                self.source = (row, column)
                print(self.source)
            elif color == COLOR["target"]:
                self.target = (row, column)
                print(self.target)
        else:
            self.itemconfig(num, fill=COLOR["empty"], outline=COLOR["empty"] if self.maze else COLOR["border"])
            if (row, column) == self.target:
                self.target =()
            elif (row, column) == self.source:
                self.source = ()
            else:
                self.map[row][column] = int(not self.map[row][column])

    def drawPath(self, heu: str = "sld", d: int = 8, animate=1):
        """
        Draw the path
        :param heu: Type of heuristic : "sld", "mht", "che", "dia", "0"
        :param d: Number of direction should be 8 or 4
        :return: None
        """
        for node in self.expanded:
            if (node[0], node[1]) != self.target and (node[0], node[1]) != self.source:
                self.itemconfig(self.grid[node[0]][node[1]].num,
                                fill=COLOR["empty"], outline=COLOR["empty"] if self.maze else COLOR["border"])
        self.path.clear()
        self.expanded.clear()
        self.path, self.expanded, self.cost, self.cnt = AStar(self.map, self.source, self.target, heu, d if not self.maze else 4)
        if self.path is None:
            tkinter.messagebox.showerror("No Route Founded !", "No path founded !")
        else:
            for node in self.expanded:
                if node == self.target or node == self.source:
                    continue
                self.itemconfig(self.grid[node[0]][node[1]].num, fill=COLOR["expanded"], outline=COLOR["expanded"] if self.maze else COLOR["border"])
                if animate:
                    self.after(1)
                    self.update()

            for node in self.path[1:-1]:
                self.itemconfig(self.grid[node[0]][node[1]].num, fill=COLOR["path"], outline=COLOR["path"] if self.maze else COLOR["border"])
                if animate:
                    self.after(1)
                    self.update()

    def GenerateMaze(self, exit=False, animate=1):
        self.clearMap()
        self.maze = True
        for r in range(len(self.map)):
            for c in range(len(self.map[0])):
                self.grid[r][c].switch()
                self.itemconfig(self.grid[r][c].num, fill=COLOR["block"], outline=COLOR["block"] if self.maze else COLOR["border"])
                self.map[r][c] = 0
        path = BackTracking(self.map)
        # print(path)
        start = 0
        if exit:
            self.itemconfig(self.grid[path[0][0]][path[0][1]].num, fill=COLOR["exit"], outline=COLOR["exit"] if self.maze else COLOR["border"])
            self.after(1)
            self.update()
            self.target = (path[0][0], path[0][1])
            start = 1
        # self.itemconfig(self.grid[path[0][0]][path[0][1]].num, fill=COLOR["exit"], outline=COLOR["exit"] if self.maze else COLOR["border"])
        # self.after(1)
        # self.update()
        # self.target = (path[0][0], path[0][1])
        # prev = path[0]
        for coords in path[start:]:
            self.grid[coords[0]][coords[1]].switch()
            self.itemconfig(self.grid[coords[0]][coords[1]].num, fill=COLOR["empty"], outline=COLOR["empty"] if self.maze else COLOR["border"])
            # self.itemconfig(self.grid[prev[0]][prev[1]].num, fill=COLOR["empty"], outline=COLOR["empty"] if self.maze else COLOR["border"])
            # prev = coords
            if animate:
                self.after(1)
                self.update()
        # self.grid[prev[0]][prev[1]].switch()
        # self.itemconfig(self.grid[prev[0]][prev[1]].num, fill=COLOR["empty"], outline=COLOR["empty"] if self.maze else COLOR["border"])
        # self.after(10)
        # self.update()
        # for r in self.map:
        #     print(r)

    def clearMap(self):
        """
        Clear the grid
        :return: None
        """
        self.maze = False
        for row in range(len(self.map)):
            for column in range(len(self.map[0])):
                self.grid[row][column].fill = False
                self.map[row][column] = 1
                self.itemconfig(self.grid[row][column].num, fill=COLOR["empty"], outline=COLOR["border"])
        self.path.clear()
        self.expanded.clear()

    def saveMap(self, filepath):
        """
        Save current view of the grid in png type
        :param filepath: The path and the name you wish to save as
        :return: None
        """
        image = Image.new("RGB", (self.__rowNum, self.__colNum))
        for row in range(self.__rowNum):
            for column in range(self.__colNum):
                if self.map[row][column] == 0:
                    image.putpixel((column, row), ImageColor.getcolor(COLOR["block"], "RGB"))
                elif (row, column) == self.target:
                    image.putpixel((column, row),
                                   ImageColor.getcolor(COLOR["target"], "RGB") if not self.maze
                                   else ImageColor.getcolor(COLOR["exit"], "RGB"))
                elif (row, column) == self.source:
                    image.putpixel((column, row), ImageColor.getcolor(COLOR["source"], "RGB"))
                elif (row, column) in self.path:
                    image.putpixel((column, row), ImageColor.getcolor(COLOR["path"], "RGB"))
                elif (row, column) in self.expanded:
                    image.putpixel((column, row), ImageColor.getcolor(COLOR["expanded"], "RGB"))
                elif self.map[row][column] == 1:
                    image.putpixel((column, row), ImageColor.getcolor(COLOR["empty"], "RGB"))
        image.save(filepath)
        tkinter.messagebox.showinfo("Save", "The map has been saved successfully !")

    def loadMap(self, img):
        pix = img.load()
        self.maze = messagebox.askyesno("Maze ?", "Is this a maze map ?")
        for r in range(self.__rowNum):
            for c in range(self.__colNum):
                if pix[r, c] == ImageColor.getcolor(COLOR["target"], "RGB"):
                    self.target = (c, r)
                    self.grid[c][r].switch()
                    self.itemconfig(self.grid[c][r].num, fill=COLOR["target"],
                                    outline=COLOR["target"] if self.maze else COLOR["border"])
                    print(self.target)
                elif pix[r, c] == ImageColor.getcolor(COLOR["exit"], "RGB"):
                    self.target = (c, r)
                    self.grid[c][r].switch()
                    self.itemconfig(self.grid[c][r].num, fill=COLOR["exit"],
                                    outline=COLOR["exit"] if self.maze else COLOR["border"])
                    print(self.target)
                elif pix[r, c] == ImageColor.getcolor(COLOR["source"], "RGB"):
                    self.source = (c, r)
                    self.grid[c][r].switch()
                    self.itemconfig(self.grid[c][r].num, fill=COLOR["source"],
                                    outline=COLOR["source"] if self.maze else COLOR["border"])
                    print(self.source)
                elif pix[r, c] == ImageColor.getcolor(COLOR["block"], "RGB"):
                    self.grid[c][r].switch()
                    self.itemconfig(self.grid[c][r].num, fill=COLOR["block"],
                                    outline=COLOR["block"] if self.maze else COLOR["border"])
                    self.map[c][r] = 0
                else:
                    self.itemconfig(self.grid[c][r].num,
                                    outline=COLOR["empty"] if self.maze else COLOR["border"])

    def __zoom(self, event):
        x, y = self.canvasx(event.x), self.canvasy(event.y)
        self.scale(ALL, x, y, 1.001 ** event.delta, 1.001 ** event.delta)

if __name__ == '__main__':
    pass