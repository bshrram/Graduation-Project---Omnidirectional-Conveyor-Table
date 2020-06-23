from cell import Cell

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
        self.append(Cell(cell))

    def getCellByLocation(self, location):
        myCell = next((i for i in self.cells if i.location == location), None)
        return myCell