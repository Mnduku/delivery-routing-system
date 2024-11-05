import datetime
# Vehicle class that is instantiated with all the necessary variables
# Represents good use of encapsulation
class Truck:
    def __init__(self, id, max_load, velocity, cargo, shipments, distance_travelled, departure_time, current_time,
                 current_address, required_packages):
        self.id = id  # Add the id attribute
        self.max_load = max_load
        self.velocity = velocity
        self.cargo = cargo
        self.shipments = shipments
        self.distance_travelled = distance_travelled
        self.current_address = current_address
        self.departure_time = departure_time
        self.current_time = current_time
        self.total_distance = 0.0  # Initialize total distance to zero
        self.required_packages = required_packages

    def showdata(self):
        print(f"\n=========TRUCK {self.id}===========")
        print(f"Departure time: {self.departure_time}")
        print(f"Package count: {self.cargo}")
        print(f"Packages: {self.shipments}")
        print(f"Distance travelled: {self.distance_travelled:.2f}")
        for f in self.required_packages: print(f.pid)
