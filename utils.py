# Created by: Michael Nduku
# Student ID: 004636371
# Date created: 10/24/2024
# WGU UPS Algorithm Project
import re
import pandas as pd
import openpyxl
import datetime
from hashtable import HashTable
from truck import Truck
from package import Package

# Helper class with all the utility operations required to run the service
class Utils():
    
    # Change address format to match that of the package files listed addresses
    # O(n) each
    def parse_address_row(address):
        match = re.search(r"\d[^,]*,", address)  # Finds from first number to the next comma
        if match:
            return match.group().strip('\n').strip().replace(',', '').replace('Station', 'Sta').replace(' W ', ' West ').replace(' E ', ' East ').replace(' S ', ' South ').replace(' N ', ' North ').replace(r" W'$", ' West').replace(r" E$", ' East').replace(r" S$", ' South').replace(r" N$",' North')
        
    def parse_address_col(address):
        match = re.search(r"\d[^\n]*", address)
        if match:
            return match.group().strip('\n').strip().replace(',', '').replace('Station', 'Sta').replace(' W ', ' West ').replace(' E ', ' East ').replace(' S ', ' South ').replace(' N ', ' North ').replace(r" W'$", ' West').replace(r" E$", ' East').replace(r" S$", ' South').replace(r" N$",' North')
        
          # Removes all periods  # Return the matched part, without newline
        return address

    # Reads the distance excel spreadsheet into a matrix where the indicies are the location names
    # 2D arrays is chosen due to the type of graph being read
    # O(m * n) where m and n are dependant on the size of the spreadsheet
    def filldistances(path):
        distance_map = pd.read_excel(path, skiprows=7, index_col=0, usecols="A,C:Z")
        distance_map.index = distance_map.index.map(Utils.parse_address_row)
        distance_map.columns = distance_map.columns.map(Utils.parse_address_col)

        print(distance_map.index)
        return distance_map

    # Reads the excel spreadsheet file line by line and creates package objects with the data
    # O(n) where n is the amount of lines in the spreadsheet
    def filltable(path):
            table = HashTable()

            # Reads the package file
            packagefile = path
            packages = pd.read_excel(packagefile, skiprows=7)
            
            # Inserts packages into hashtable
            for _, row in packages.iterrows():
                try:
                    pid = int(row['Package\nID'])
                    address = row['Address']
                    if address == '3575 W Valley Central Station bus Loop': 
                        address = '3575 W Valley Central Sta bus Loop' #The adresses were different in the package and distancee file so I had to add this. 
                    city = row['City ']
                    zipcode = row['Zip']
                    deadline = row['Delivery\nDeadline']
                    weight = row['Weight\nKILO']
                    notes = row['page 1 of 1PageSpecial Notes']  

                    # Use data to initialize instance of package class
                    package = Package(pid, address, city, zipcode, deadline, weight, 'At hub', notes)
                    table._insert(pid, package)
                
                except Exception as e:
                    print(f"An exception occurred: {e}")
                    continue
            return table

    # Calculates the distance between addresses
    # Ensures both addresses are not none and that their distance is found in the distance matrix
    # O(n) since declaring the set processes them all once
    def calculate_distance(id1, id2, distance_map):
        if id1 in distance_map:
            address1 = id1
        else:
            address1 = None
        if id2 in distance_map:
            address2 = id2
        else:
            address1 = None

        distance = distance_map[id1][id2]
        if distance is None: distance = distance_map [id2][id1]

        if distance is None:
            print(f"Warning: Distance between {id1} and {id2} is undefined.")
            return address1, address2, None

        return distance


    # Locates a package and returns its status by using the id as a key for the hashtable
    # 0(1) complexity because it only has to search the given keys value
    def status(hashtable, pid, time):
        package = hashtable.get(pid)
        if package:
            package.update_status(time)
            return package.status
        else:
            return f"Could not find package with id {pid}"


    def get_delivery_details(package):
        # Prints out delivery details for a package

        k = ["Package ID", "Address", "City", "State", "Zip Code", "Deadline",
                "Weight", "Notes", "Status"]
        v = [package.package_id, package.address, package.city, package.state,
                package.zip_code, package.deadline, package.weight, package.notes,
                package.status]

        details = ""
        for i in range(len(k)):
            # Cycle through the colors 31-36
            color_code = 31 + (i % 6)
            details += f"\033[{color_code}m{k[i]}: {v[i]}, "
        details += "\033[0m"  # Reset color
        return details

    # To find the best route to deliver the packages, we use a recursive algorith
    # The deliver algorith will keep calling itself thus branching out into every possible delivery order
    # Due to the function being called recursively we can check if each route was more efficient then the current best route to come out with the best solution
    # This function is O()
    def route(truck, hashtable, distance_map):
        
        priority_package = []  # packages with a deadline before EOD
        regular_package = []  # packages with a delivery deadline of EOD

        # Separate packages with deadlines from packages without deadlines
        for i in range(1, hashtable.size):
            package = hashtable._get(i)

            if package.deadline == 'EOD':
                regular_package.append(package)
            else:
                priority_package.append(package)

        truck.shipments.clear()
        total_distance = 0.00

        def deliver(packages):

            nonlocal total_distance

            while len(packages) > 0:
                next_address = 1e308
                next_package = None

                # Retreives the adress of both the truck and the package to calculate the distance between them
                closest_delivery = 1000  
                for thispackage in packages:
                    package_address = thispackage.address
                    truck_address = truck.current_address
                    distance = Utils.calculate_distance(truck_address, package_address, distance_map)
                    
                    # Set the next package to the closest package
                    if distance <= closest_delivery:
                        closest_delivery = distance
                        next_package = thispackage
                        next_address = next_package.address

                # Find delivery times for next package
                if next_package:
                    if next_package.departure_time is None:
                        next_package.departure_time = truck.current_time
                        next_package.delivery_time = truck.current_time

                else:
                    return truck, total_distance

                # Mark the package as on the way, thus removing it from the has
                # htable so its not delivered twice
                next_package.status = "On the way"
                mileage = Utils.calculate_distance(truck_address, next_address, distance_map)
                delivery_time = truck.current_time + datetime.timedelta(hours=  mileage / truck.velocity)
                print(f"Truck has completed its delivery to {truck.current_address} and is on it's way to drop off a package at {next_package.address}")
                print(f"Expected arrival time is {delivery_time}")

                truck.shipments.append(next_package.pid)
                packages.remove(next_package)

                # If the truck has moved, we find the travel time using the formula time = distance / velocity
                # We then add this to the total distance so we can keep track of how long the route has taken in total
                if truck.current_address != next_package.address:
                    truck.current_time = delivery_time
                    total_distance += mileage

                    next_package.status = "Delivered"
                    next_package.delivered = True

                truck.current_address = next_package.address

        # Function recursively calls itself and breaks out when all packages are delivered
        deliver(priority_package)
        deliver(regular_package)

        # Record how long the route took in total
        truck.total_distance = total_distance
        return truck, total_distance

    # Calculates the return time of a truck from its final delivery and returns how far it is
    def calculate_return(truck, truck_address, start_location, distance_map):
        distance = Utils.calculate_distance(truck_address, start_location , distance_map)
        return_time = datetime.timedelta(hours= (distance / truck.velocity))
        print(truck.current_time)
        truck.current_time = truck.current_time + return_time
        truck.total_distance += distance

        return truck, truck.current_time


