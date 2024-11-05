# Package class contains properties of the packages from the excel spreadsheet
from datetime import datetime, date, timezone
import pytz
class Package:
    def __init__(self, pid, address, city, state, zipcode, deadline, weight, notes):
        self.status = None
        self.pid = pid
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zipcode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.departure_time = None
        self.load_time = None
        self.delivery_time = None
        self.status = "dock"
        which_truck = None

    def return_status(self, checktime):
        # Printing statement logic for the status of a package at a given time
        if self.delivery_time != None and (self.delivery_time) <=  (checktime):
            return(f"Package #{self.pid} was delivered by truck {self.which_truck} at {self.delivery_time}")
        elif self.load_time != None and checktime >= self.load_time:
            return(f"Package #{self.pid} was loaded into truck {self.which_truck} at {self.load_time} and is currently en route")
        else:
            return(f"Package #{self.pid} is still at the dock and waiting to be loaded")