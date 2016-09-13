
from copy import deepcopy
from copy import copy
import random

class Grid(object):
    def __init__(self, rows, columns, fillValue = None):
        self._data = Array(rows)
        for row in range(rows):
            self._data[row] = Array(columns, fillValue)

    def getHeight(self):
        return len(self._data)

    def getWidth(self):
        return len(self._data[0])

    def __getitem__(self, index):
        return self._data[index]

    def __str__(self):
        result = ""
        for row in range(self.getHeight()):
            for col in range(self.getWidth()):
                entry =  str(self._data[row][col])
                result += (" " if entry == "" else entry) + ""
            result += "\n"
        return result

class Array(object):
    def __init__(self, capacity, fillValue = None):
        self._items = list()
        for count in range(capacity):
            self._items.append(fillValue)

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return str(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __setitem__(self, index, newItem):
        self._items[index] = newItem

def insertword(grid, word, x, y, vertical):
    tempgrid = deepcopy(grid)
    allowed = True
    for i in range(0, len(word)):
        if x >= tempgrid.getWidth() or y >= tempgrid.getHeight(): # out of bounds
            allowed = False
        elif tempgrid[x][y] != "" and tempgrid[x][y] != word[i]: # diff letter
            allowed = False
        # these are all adjacency checks
        elif tempgrid[x][y] == "" and vertical and x-1 >= 0 and tempgrid[x-1][y] != "":
            allowed = False
        elif tempgrid[x][y] == "" and vertical and x+1 < tempgrid.getWidth() and tempgrid[x+1][y] != "":
            allowed = False
        elif tempgrid[x][y] == "" and not vertical and y-1 >= 0 and tempgrid[x][y-1] != "":
            allowed = False
        elif tempgrid[x][y] == "" and not vertical and y+1 < tempgrid.getHeight() and tempgrid[x][y+1] != "":
            allowed = False
        # these are all checks that we're not overlapping with another word in same dir
        elif i==0 and not vertical and x-1 >= 0 and tempgrid[x-1][y] != "":
            allowed = False
        elif i== len(word)-1 and not vertical and x+1 < tempgrid.getWidth() and tempgrid[x+1][y] != "":
            allowed = False
        elif i==0 and vertical and y-1 >= 0 and tempgrid[x][y-1] != "":
            allowed = False
        elif i== len(word)-1  and vertical and y+1 < tempgrid.getHeight() and tempgrid[x][y+1] != "":
            allowed = False
        else:
            tempgrid[x][y] = word[i]

        if vertical:
            y += 1
        else:
            x += 1

        if not allowed:
            tempgrid = deepcopy(grid)
            break

    return [allowed, tempgrid]

def gridQualityMetric(grid):
    quality = 0.0
    for x in range(grid.getWidth()):
        for y in range(grid.getHeight()):
            xlink = False
            ylink = False
            if grid[x][y] != "":
                if x-1 >= 0 and grid[x-1][y] != "":
                    xlink = True
                if x+1 < grid.getWidth() and grid[x+1][y] != "":
                    xlink = True
                if y-1 >= 0 and grid[x][y-1] != "":
                    ylink = True
                if y+1 < grid.getHeight() and grid[x][y+1] != "":
                    ylink = True
            quality += 1 if xlink and ylink else 0

    return quality

fname = "./words.txt"

words = [line.strip() for line in open(fname)]

maxlength = 0;

for word in words:
    if len(word) > maxlength:
        maxlength = len(word)


maxquality=0
bestgrid = Grid(maxlength, maxlength, "")

for i in range(0,1000000):
    tempwords = deepcopy(words)
    grid = Grid(maxlength, maxlength, "")
    numwords=0


    for j in range(0,20000):
        if len(tempwords) > 1:
            randword = random.randint(0, len(tempwords)-1)
            randx = random.randint(0, maxlength-1)
            randy = random.randint(0, maxlength-1)
            vertical = True if random.randint(0, 1) == 0 else False

            tryinsert = insertword(grid, tempwords[randword], randx, randy, vertical)
            if tryinsert[0]:
                grid = tryinsert[1]
                tempwords.pop(randword)
                numwords += 1

    if gridQualityMetric(grid) >= maxquality:
        print("Candidate: ", gridQualityMetric(grid), "\n")
        print(grid)
        print("**********************************************************")

    if gridQualityMetric(grid) > maxquality:
        bestgrid = deepcopy(grid)
        maxquality = gridQualityMetric(grid)


print(" - - - - - - - - - - - - - ")
print("Best: ", maxquality)
print(bestgrid)
