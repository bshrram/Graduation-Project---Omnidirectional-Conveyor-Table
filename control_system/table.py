from cell import Cell
from common import *
import math

row = 4
col = 10
class Table:
    """Table class that contains cells
    Attributes:
        None
    """

    def __init__(self, cells):
        """Initialize variables used by Table class
        Args:
            cells: list of cells objects
        """
        self.cells = []
        for i in range(len(cells)):
            self.cells.append(Cell(cells[i]))

    def addCell(self, cell):
        """Add cell to tabel.cells
            Args:
                cell: cell object
        """
        self.cells.append(Cell(cell))

    def getCellByLocation(self, location):
        """location: list
        """
        [x, y] = location
        if x>=row or x<0 or y<0 or y>=col:
            return None
        myCell = next((i for i in self.cells if i.location == location), None)
        return myCell

    def getCommonCells(self, cell):
        id = int(cell.id/10)
        commCells = [cell for cell in self.cells if int(cell.id/10) == id]
        # print(commCells)
        return commCells

    def getCellsByNearLocation(self, location, howMany):
        distance = []
        for i in range(20):
            r = calculateDistance(location, self.cells[i].coordinates)
            distance.append((r, i))
        distance.sort()
        distance=distance[:howMany]
        result = []
        for i in range(howMany):
            result.append(self.cells[distance[i][1]])
            # print((distance[i][0], result[i].location, result[i].coordinates))
        return result

    def getAngle(self, startLocation, endLocation):
        (x1, y1) = startLocation
        (x2, y2) = endLocation
        x = x2 - x1
        y = y1 - y2
        a = math.atan2(y, x)
        a = math.degrees(a)
        a -= 90
        if a <0:
            a = 360 + a
        return a
    
    def goToCell(self, cell, cells, boxCenter):
        speed = 170
        runningCells = []
        for i in range(len(cells)):
            comCells = self.getCommonCells(cells[i])
            if (cell.id == cells[i].id):
                angle = self.getAngle(boxCenter, cell.coordinates)
                self.move(cell, angle, speed, 0)
                runningCells += comCells
                continue
            angle  = self.getAngle(cells[i].coordinates, cell.coordinates)
            self.move(cells[i], angle, speed, 0)
            runningCells += comCells

        restCells = [cell for cell in self.cells if cell not in runningCells]
        for i in range(len(restCells)):
            if restCells[i].getStatus() == (-1, -1, -1):
                continue
            comCells = self.getCommonCells(restCells[i])
            restCells[i].stop(comCells)

    def goToLocation(self, location, cells, centersMM):
        speed = 175
        runningCells = []
        for i in range(len(cells)):
            comCells = self.getCommonCells(cells[i])
            angle  = self.getAngle(centersMM, location)
            cells[i].move(angle, speed, 0, comCells)
            runningCells += comCells

        restCells = [cell for cell in self.cells if cell not in runningCells]
        for i in range(len(restCells)):
            if restCells[i].getStatus() == (-1, -1, -1):
                continue
            comCells = self.getCommonCells(restCells[i])
            restCells[i].stop(comCells)

            
    def move(self, cell, angle, speed, w):
        comCells = self.getCommonCells(cell)
        cell.move(angle, speed, w, comCells)

    def rotate(self, cell, angle):
        self.move(cell, 0, 0, )