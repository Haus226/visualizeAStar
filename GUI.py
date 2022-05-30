from Canvas import CellGrid
from tkinter import colorchooser, filedialog, ttk
import tkinter
import PIL.Image
from utils import *


class Console:
    __HEU = ("sld", 8)

    def __init__(self, rowNumber, columnNumber, CellSize):
        self.__cellSize, self.__rNum, self.__cNum = CellSize, rowNumber, columnNumber

        self.__app = Tk()
        self.__app.title("A* Algorithm")
        self.__app.geometry("700x600")
        self.__frame = Frame(self.__app)
        heu_label = Label(self.__app, text="Heuristic : Euclidean Dist. 8", font=("Aerial", 18))
        heu_label.pack()
        pathInfo_label = Label(self.__app, text=f"Expanded : 0 Cost : 0", font=("Aerial", 18))
        pathInfo_label.pack()

        self.__frame.pack()
        frameInfo = Frame(self.__frame)
        frameInfo.pack(side=RIGHT)

        self.__canvas = CellGrid(self.__frame, rowNumber, columnNumber, CellSize)
        self.__canvas.pack()

        text = ["Block", "Source", "Target", "Path", "Expanded", "Exit", "Empty"]
        clabel = tlabel = []

        for cnt in range(len(text)):
            colorLabel = Label(frameInfo, bg=COLOR[text[cnt].lower()], width=4, height=2, name=text[cnt].lower(), cursor="exchange")
            colorLabel.grid(row=cnt, column=0)
            textLabel = Label(frameInfo, text=text[cnt], height=2, font=("Aerial", 12))
            textLabel.grid(row=cnt, column=1)
            clabel.append(colorLabel)

        menu = Menu(self.__app)

        AStarMenu = Menu(menu, tearoff=0)
        AStarMenu.add_radiobutton(label="Euclidean Distance 8", command=lambda: self.__configAStar("sld", heuLabel=heu_label))
        AStarMenu.add_radiobutton(label="Manhattan Distance 8", command=lambda: self.__configAStar("mht", heuLabel=heu_label))
        AStarMenu.add_radiobutton(label="Chebyshev Distance 8", command=lambda: self.__configAStar("che", heuLabel=heu_label))
        AStarMenu.add_radiobutton(label="Diagonal Distance 8", command=lambda: self.__configAStar("dia", heuLabel=heu_label))
        AStarMenu.add_radiobutton(label="Dijkstra 8", command=lambda: self.__configAStar("0", heuLabel=heu_label))
        AStarMenu.add_separator()
        AStarMenu.add_radiobutton(label="Euclidean Distance 4", command=lambda: self.__configAStar("sld", 4, heu_label))
        AStarMenu.add_radiobutton(label="Manhattan Distance 4", command=lambda: self.__configAStar("mht", 4, heu_label))
        AStarMenu.add_radiobutton(label="Chebyshev Distance 4", command=lambda: self.__configAStar("che", 4, heu_label))
        AStarMenu.add_radiobutton(label="Diagonal Distance 4", command=lambda: self.__configAStar("dia", 4, heu_label))
        AStarMenu.add_radiobutton(label="Dijkstra 4", command=lambda: self.__configAStar("0", 4, heu_label))
        menu.add_cascade(label="Configure", menu=AStarMenu)

        ToolsMenu = Menu(menu, tearoff=0)
        self.__animate = IntVar()
        ToolsMenu.add_command(label="Save    | Ctrl + Shift + S", command=self.__save)
        ToolsMenu.add_command(label="Load    | Ctrl + Shift + A", command=lambda: self.__load(labelList=clabel))
        ToolsMenu.add_command(label="Resize  | Ctrl + Shift + Q", command=lambda: self.__resizeCanvas(autoChange=False))
        ToolsMenu.add_command(label="Run     | Ctrl + Shift + Z", command=self.__run)
        ToolsMenu.add_command(label="Clear   | Ctrl + Shift + X", command=self.__clear)
        ToolsMenu.add_separator()
        ToolsMenu.add_checkbutton(label="Animation", offvalue=0, onvalue=1, variable=self.__animate)

        menu.add_cascade(label="Tool", menu=ToolsMenu)

        self.__app.config(menu=menu)

        tkinter.ttk.Style().configure("TButton", font=("Aerial", 12), width=15)
        resizeCanvas = tkinter.ttk.Button(frameInfo, text="Resize Grid", command=lambda: self.__resizeCanvas(autoChange=False))
        resizeCanvas.grid(row=7, columnspan=2, column=0)
        generateMaze = tkinter.ttk.Button(frameInfo, text="Generate Maze", command=self.__generateMaze)
        generateMaze.grid(row=8, columnspan=2, column=0)
        runAStar = tkinter.ttk.Button(frameInfo, text="Run A*", command=lambda: self.__run(pathInfo_label))
        runAStar.grid(row=9, columnspan=2, column=0)
        clear = tkinter.ttk.Button(frameInfo, text="Clear", command=lambda: self.__clear(pathInfo_label))
        clear.grid(row=10, column=0, columnspan=2)

        self.__app.bind("<Control-Shift-S>", self.__save)
        self.__app.bind("<Control-Shift-A>", lambda e: self.__load(e, clabel))
        self.__app.bind("<Control-Shift-Z>", self.__run)
        self.__app.bind("<Control-Shift-X>", self.__clear)
        self.__app.bind("<Control-Shift-Q>", lambda e: self.__resizeCanvas(e, autoChange=False))
        self.__app.bind("<Control-Shift-W>", self.__generateMaze)

        for label in clabel:
            label.bind_all()
            label.bind("<Button-1>", self.__colorPicker)
        self.__app.mainloop()

    def __resizeCanvas(self, e=None, autoChange=True, r=None, c=None):

        if not autoChange:
            r_c_s = resizeDialog(self.__app)
            if r_c_s[0].get() != "" and r_c_s[1].get() != "" and r_c_s[2].get() != "":
                self.__canvas.destroy()
                self.__rNum, self.__cNum = int(r_c_s[0].get()), int(r_c_s[1].get())
                self.__canvas = CellGrid(self.__frame, int(r_c_s[0].get()), int(r_c_s[1].get()), int(r_c_s[2].get()))
                self.__canvas.pack()
        else:
            self.__canvas.destroy()
            self.__rNum, self.__cNum = r, c
            self.__canvas = CellGrid(self.__frame, r, c, 12)
            self.__canvas.pack()

    def __colorPicker(self, e):
        global COLOR
        color = colorchooser.askcolor(title="Colour Picker")
        if e.widget.winfo_name() != "empty":
            COLOR[e.widget.winfo_name()] = color[1]
            e.widget.configure(bg=color[1])
            if e.widget.winfo_name() == "block":
                for r in range(len(self.__canvas.map)):
                    for c in range(len(self.__canvas.map[0])):
                        if not self.__canvas.map[r][c]:
                            self.__canvas.itemconfig(self.__canvas.grid[r][c].num, fill=color[1])
        else:
            COLOR[e.widget.winfo_name()] = color[1]
            e.widget.configure(bg=color[1])
            for r in range(len(self.__canvas.map)):
                for c in range(len(self.__canvas.map[0])):
                    if self.__canvas.map[r][c]:
                        self.__canvas.itemconfig(self.__canvas.grid[r][c].num, fill=COLOR["empty"],
                                                 outline=COLOR["empty"] if self.__canvas.maze else COLOR["border"])

    def __configAStar(self, method="sld", d=8, heuLabel: Label = None):
        if method == "sld":
            heuLabel.config(text=f"Heuristic : Euclidean Dist. {d}")
        elif method == "mht":
            heuLabel.config(text=f"Heuristic : Manhattan Dist. {d}")
        elif method == "che":
            heuLabel.config(text=f"Heuristic : Chebyshev Dist. {d}")
        elif method == "dia":
            heuLabel.config(text=f"Heuristic : Diagonal Dist. {d}")
        elif method == "0":
            heuLabel.config(text=f"Heuristic : None (Dijkstra) {d}")
        self.__HEU = (method, d)

    def __generateMaze(self, e=None):
        self.__canvas.GenerateMaze(animate=self.__animate.get())

    def __run(self, pathInfo_label: Label, event=None):
        self.__canvas.drawPath(self.__HEU[0], self.__HEU[1], animate=self.__animate.get())
        pathInfo_label.config(text=f"Expanded : {self.__canvas.cnt} Cost : {self.__canvas.cost}")

    def __load(self, event=None, labelList=None):
        filename = filedialog.askopenfilename(
            title="Open your map",
            filetypes=(
                (".png", "*.png"),
            )
        )
        print(filename)
        img = PIL.Image.open(filename, "r")
        row, column = img.size
        if (column, row) != (self.__rNum, self.__cNum):
            self.__resizeCanvas(r=column, c=row)
        readPrevColor(filename.replace("png", "csv"))
        self.__canvas.loadMap(img)
        for label in labelList:
            label.configure(bg=COLOR[label.winfo_name()])

    def __save(self, event=None):
        filename = filedialog.asksaveasfile(
            defaultextension=".png",
            filetypes=(
                (".png", "*.png"),
            ),
        ).name
        savePrevColor(filename.replace("png", "csv"))
        self.__canvas.saveMap(filename)

    def __clear(self, pathInfo_label: Label, event=None):
        self.__canvas.clearMap()
        pathInfo_label.config(text=f"Expanded : 0 Cost : 0")


if __name__ == '__main__':
    Console(9, 9, 15)

