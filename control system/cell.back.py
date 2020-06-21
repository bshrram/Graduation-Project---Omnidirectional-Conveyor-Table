from motor import Motor


class Cell:
    """Cell class that represents a cell in table
    Attributes:
      None
    """

    def __init__(self, cell):
        """Initialize variables used by Cell class
        Args:
            cell: dict represents a cell data:
                cell.id: int 
                cell.location: tuple
                cell.motors: list of objects
        """
        self.id = cell.id
        self.location = cell.location
        self.motors = []
        self.angle = self.magnitude = self.w = -1
        for i in range(len(cell.motors)):
            self.motors.append(
                Motor({**cell.motors[i], "id": self.id * 10 + i}))
        
        def getStatus(self):
            return (self.angle, )

        def move(self, angle, magnitude, w):
            #Todo @ali
            pass 

        def stop(self):
            #Todo
            pass

