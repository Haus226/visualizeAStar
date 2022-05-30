# Console that visualizes A* Searching

## Snapshots:

[<img src="/snapshots/GUI.png" width="256" height="256">](./snapshots/GUI.png)
[<img src="/snapshots/Customize.png" width="256" height="256">](./snapshots/Customize.png)
[<img src="/snapshots/Colour Picker.png" width="256" height="256">](./snapshots/Colour Picker.png)

[<img src="/snapshots/Resize.png" width="256" height="256">](./snapshots/Resize.png)
[<img src="/snapshots/Generate Maze.png" width="256" height="256">](./snapshots/Generate Maze.png) 
[<img src="/snapshots/Path.png" width="256" height="256">](./snapshots/Path.png) 

[//]: # ([<img src="/snapshots/Running.png" width="256" height="256">]&#40;./snapshots/Running.png&#41; )


## Introduction:
There are totally 7 python scripts for the whole project which are `Canvas.py`, `SearchAlgo.py`, `MazeAlgo.py`, 
`GUI.py`, `utils.py` `config.py`, `run.py`\
The implementation of A* algorithm is in [SearchAlgo.py](SearchAlgo.py), implementation of Maze Generating Algorithm is in [MazeAlgo.py](MazeAlgo.py) 
while the GUI is in [GUI.py](GUI.py)


## A* Algorithm

| Heuristic Function | Choice of Directions |
|:-------------------|:--------------------:|
 | Euclidean Dist.    |        4 & 8         |
 | Manhattan Dist.    |        4 & 8         |
 | Chebyshev Dist.    |        4 & 8         |
 | Diagonal Dist.     |        4 & 8         |
 | None <==> Dijkstra |        4 & 8         |


## Maze Generating Algorithm

| Maze Algorithm                           |
|:-----------------------------------------|
| Backtracking or Iterative DFS            |
| Randomized Kruskal's Algo. (Coming Soon) |
| Randomized Prim's Algo. (Coming Soon)    |

### Maze Generated :

[<img src="/snapshots/maze64 screenshot.png" width="256" height="256">](./snapshots/maze64 screenshot.png)
[<img src="/snapshots/maze128 screenshot.png" width="256" height="256">](./snapshots/maze128 screenshot.png)




| Modules               | Usage                                                           |
|:----------------------|:----------------------------------------------------------------|
| math (inf, sqrt)      | Calculation of heuristic values and Initialization of algorithm |
| PIL (Image)           | Save and Load images                                            |
| queue (PriorityQueue) | Use Priority Queue in implementation of algorithm               |
| tkinter               | GUI                                                             |
| random                | Implementation of maze                                          |


### Run :
1) Set the default colours of different types of blocks in [config.py](config.py) such as Target, Source, Block etc.
   * *Colours of the blocks can be changed by clicking on the coloured square and choose the colour you liked with colour picker provided.* *
2) Run the [run.py](run.py) script and start to play !
   * *To see the animation, remember to click the "Tool" menu and choose the "Animate" checkbutton.*
   
***Remark: The column and row number should less than 250 and both are odd to get the best experience.***


### References : 
1) [Heuristic functions](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html) 
2) [2D Grid](https://stackoverflow.com/questions/30023763/how-to-make-an-interactive-2d-grid-in-a-window-in-python)
    - *Originally, this implementation is not changing the colour of the rectangle created but create a new rectangle 
   with the new colour and cover the original one. Thus, I modify the codes so that the original rectangle will be modified
   not covered.*
    - *At the same time, I also modify the ***_eventCoords function*** so that it is compatible with zooming.*
3) [Zooming](https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan)
4) [Maze Algorithm](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap.html)

### Shortcuts and Events :

| Events             | Function                         |
|:-------------------|:---------------------------------|
| Right Click        | Add destination or target        |
| Left Click or Drag | Add blockage                     | 
| Middle Click       | Add starting point               |
| MouseWheel         | Zoom the grid                    |
| Ctrl + Shift + S   | Save the current grid as png     |
| Ctrl + Shift + A   | Load the saved grid png file     |
| Ctrl + Shift + Z   | Run the path searching algorithm |
| Ctrl + Shift + X   | Clear the current grid           | 
| Ctrl + Shift + Q   | Resize the grid                  |
| Ctrl + Shift + W   | Generate maze                    |