# Package class contains properties of the packages from the excel spreadsheet
from datetime import datetime, date
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

    def update(self, convert_datetime):
        # Convert datetime to timedelta since midnight
        convert_timedelta = datetime.combine(date.min, convert_datetime.time()) - datetime.min

        if self.delivery_time is not None and self.delivery_time < convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time is not None and self.departure_time > convert_timedelta:
            self.status = "En route"
        else:
            self.status = "At Hub"
