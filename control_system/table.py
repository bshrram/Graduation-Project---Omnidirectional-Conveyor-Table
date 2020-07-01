from cell import Cell
from common import *
import math

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
            print((distance[i][0], result[i].location, result[i].coordinates))
        return result

    def getAngle(self, startCell, endCell):
        (x1, y1) = startCell.coordinates
        (x2, y2) = endCell.coordinates
        x = x2 - x1
        y = y1 - y2
        a = math.atan2(y, x)
        a = math.degrees(a)
        # if x<0 and y>=0:
        #     a += 90
        # elif x<0 and y<0:
        #     a+=180
        # elif x>=0 and y<0:
        #     a = 360 - a
        return a
    
    def goToCell(self, cell, cells):
        runningCells = []
        for i in range(len(cells)):
            comCells = self.getCommonCells(cells[i])
            angle  = self.getAngle(cells[i], cell)
            cells[i].move(angle, 250, 0, comCells)
            runningCells += comCells

        restCells = [cell for cell in self.cells if cell not in runningCells]
        for i in range(len(restCells)):
            if restCells[i].getStatus() == (-1, -1, -1):
                continue
            comCells = self.getCommonCells(restCells[i])
            restCells[i].stop(comCells)

            
        