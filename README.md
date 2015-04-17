# graphicalgs

This simple API provides some functions to help you writing **graphic representation** of some algorithms.

It uses [Pygame](www.pygame.org) for drawing.

##Usage
To use this API in your program just put the file  _**drawing.py**_ in the same folder with your  _**.py**_  file and then `import drawing`.

##Reference
###Functions
Functions defined inside this API

`drawArray(screen, array, color, horizontal, highlight, hlcolors, swap, swap_time)`
>This function calculates size to fit the surface and draws the array as an histogram with the specified color. You can specify some elements to highlight and also animate the swap of two elements.

>**Arguments:**
>+ *screen*: it's a *pygame.Surface* object, the surface where the array will be drawn on
>+ *array*: it's a *tuple* or *list* object, the array to be drawn
>+ *color*: it's a *pygame.Color* compatible object, is the color used to draw the array elements, default is **black**.
>+ *horizontal*: it's a *bool* value, `True` if you want to print the histogram horizontally; optional.
>+ *highlight*: it's a *list* containing the indexes of the elements to highlight; optional.
>+ *hlcolors*: it's a *list* containing the color used for highlight the elements; `highlight[i]` will be draw with the color in `hlcolors[i]`; if there are more elements in *highlight* than in *hlcolors* the last color will be used for elements that doesn't have a color specified; optional.
>+ *swap*: a *list* containing the **two** elements to swap; optional.
>+ *swap_time*: an *integer*, the duration of the swap animation; optional.

###Classes
Classes defined inside this API

**Node**
>This class represents a node inside a graph.

>`__init__(name, x, y, size)`

>>Class constructor.
>>+ *name*: a *string*, the label of the node, always converted in string.
>>+ *x*, *y*: the position of the node on the screen (center).
>>+ *size*: the diameter of the circle when drawn; default 30.

>`draw(screen, color)`

>>Draws the node as a circle with the label inside.
>>+ *screen*: a *pygame.Surface* object, the surface where the node will be draw on.
>>+ *color*: a *pygame.Color* compatible object, the color the node will be draw with.

**Edge**
>This class represents an edge (connecting two nodes) inside a graph.

>`__init__(nodeFrom, nodeTo, weight)`

>>Class constructor.
>>+ *nodeFrom*: a *Node* object, the starting node of the edge.
>>+ *nodeTo*: a *Node* object, the ending node of the edge.
>>+ *weight*: an *integer*, the weight of the edge, considered only in case of weighted graph; default 1.

>`draw(screen, color)`

>>Draws the edge as an anti-aliased line.
>>+ *screen*: a *pygame.Surface* object, the surface where the edge will be draw on.
>>+ *color*: a *pygame.Color* compatible object, the color the ege will be draw with.

**Graph**
>This class represents a graph, containing edges and nodes.

>`__init__(edges)`

>>Class constructor.
>>+ *edges*: it's a *list* object containing the *Edges* making the graph.

>`draw(screen, color, highlight, hlcolors)`

>>Calls the `draw` function for every node and edge inside the graph.
>>+ *screen*: the *pygame.Surface* where to draw the graph on.
>>+ *color*: the color used to draw the graph.
>>+ *highilight*, *hlcolors*: for highlighting nodes, they work as in `drawArray`.

>`genAdjList()`

>>Generates the adjacent list for this graph. Returns a dictionary where the keys are the nodes name and the values are lists containing the labels of the connected nodes.