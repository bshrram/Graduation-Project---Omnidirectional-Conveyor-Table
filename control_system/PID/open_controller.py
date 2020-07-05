##################################################################################
# This will be our control class that over the course of the next lessons will 
# become more advance!
##################################################################################

# Create an Open_Controller class!
class Open_Controller:
    # Define the class initalization sequence! 
    def __init__(self, start_time = 0):
        
        # Create a class variable to store the start time!
        self.start_time_ = start_time
        
        # Create a class variable to store the control effort!
        self.u = 0
        
        # Create a class variable to store the last timestamp!
        self.last_timestamp_ = 0
        
        # Create a class variable to store our set point!
        self.set_point_ = 0
        
        # Create a class variable to all applied control efforts!
        self.effort_applied = []

    # Set the altitude set point
    def setTarget(self, target):
        self.set_point_ = float(target)
     
    # Set the desired control effort   
    def setControlEffort(self, control_effort):
        self.u = float(control_effort)

    # Retrive the current control effort
    def getControlEffort(self,time):
        # Store the last time stamp!
        self.last_timestamp_ = time
        
        # Store control effort applied!
        self.effort_applied.append(self.u)
        
        return self.u