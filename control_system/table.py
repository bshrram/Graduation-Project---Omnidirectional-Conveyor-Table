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
    
    def goToCell(self, cell, centersMM):
        speed = 170
        numRunningCells = 4
        runningCells = []
        cells = self.getCellsByNearLocation(centersMM, numRunningCells)
        for i in range(len(cells)):
            comCells = self.getCommonCells(cells[i])
            if (cell.id == cells[i].id):
                angle = self.getAngle(centersMM, cell.coordinates)
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

    def goToLocation(self, location, centersMM):
        speed = 175
        runningCells = []
        numRunningCells = 4
        cells = self.getCellsByNearLocation(centersMM, numRunningCells)
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

    def rotate(self, cell, w):
        comCells = self.getCommonCells(cell)
        cell.move(0, 0, w, comCells)
    
    def stopCell(self, cell):
        comCells = self.getCommonCells(cell)
        cell.stop(comCells)

    def followPath(self, path, centersMM, angle, index, hanging, speed=170):
        #Todo: if end cell on right or left edge, rotate to 90
        # else if on up or down edge rotate 0

        [hang, hangFrames, dir] = hanging
        runningCells = self.getCellsByNearLocation(centersMM, 4)

        if calculateDistance(centersMM, path[index]) < 50:
            index = index+1
            if index == len(path):
                index = -1
                return [index, hang, hangFrames]

        if (hang): 
            # rotate to fix hanging in location
            # print(f'count: {count}')
            w = 140 * dir
            for i in range(len(runningCells)):
                self.rotate(runningCells[i], w)
            hangFrames -= 1
            if hangFrames == 0:
                hang = 0

        else:
            #print("move")
            self.goToLocation(path[index], centersMM)

        return [index, hang, hangFrames]
        

    def isHanging(self, hang, hangFrames, curPos, pastPos, dir1):
        dis = calculateDistance(curPos, pastPos)
        if (dis < 6):
            hangFrames += 1
            if hangFrames >= 10 and hangFrames < 250:
                hangFrames *= 2.5
                hang = 1
        else:
            dir1 *= -1
            hangFrames = 0
            hang = 0
        return [hang, hangFrames, dir1]