# Created by: Michael Nduku
# Student ID: 004636371
# Date created: 10/24/2024
# WGU UPS Algorithm Project
import re
import pandas as pd
import openpyxl
import datetime
from datetime import datetime, timedelta
from hashtable import HashTable
import numpy as np
from truck import Truck
from package import Package

# Helper class with all the utility operations required to run the service
class Utils():
    
    # Change address format to Ensure consistency between all address formats
    # O(n) each

    def convert_address(address):
        # Remove everything before the first number
        match = re.search(r'\d', address)
        if match:
            address = address[match.start():]
        else:
            return ''
        
        # Remove everything after the following newline or comma
        match = re.search(r'[\n\,]', address)
        if match:
            address = address[:match.start()]
        
        # Replace any direction will the shortened version
        replacements = {
            'West': 'W',
            'East': 'E',
            'North': 'N',
            'South': 'S',
            'Station': 'Sta'
        }
        
        # Function to replace matched directions
        def replace_direction(match):
            return replacements[match.group()]
        
        # Use regex to find and replace directions
        address = re.sub(r'\b(West|East|North|South|Station)\b', replace_direction, address)
        
        return address.strip()

    # Reads the distance excel spreadsheet into a matrix where the indicies are the location names
    # 2D arrays is chosen due to the type of graph being read
    # O(m * n) where m and n are dependant on the size of the spreadsheet
    def filldistances(path):
        distance_map = pd.read_excel(path, skiprows=7, index_col=0, usecols="A,C:AC")
        distance_map.index = distance_map.index.map(Utils.convert_address)
        distance_map.columns = distance_map.columns.map(Utils.convert_address)
        return distance_map

    # Reads the excel spreadsheet file line by line and creates package objects with the data
    # O(n) where n is the amount of lines in the spreadsheet
    # Option variable determines if we are filling the list or table
    def filltable(path, option):
            if option == 0:
                table = HashTable()
            else:
                table = []
            # Reads the package file
            packagefile = path
            packages = pd.read_excel(packagefile, skiprows=7)
            
            # Inserts packages into hashtable
            for _, row in packages.iterrows():
                try:
                    pid = int(row['Package\nID'])
                    address = row['Address']
                    city = row['City ']
                    state = row['State']
                    zipcode = row['Zip']
                    deadline = row['Delivery\nDeadline']
                    weight = row['Weight\nKILO']
                    notes = row['page 1 of 1PageSpecial Notes']  

                    # Use data to initialize instance of package class
                    address = Utils.convert_address(address)
                    package = Package(pid, address, city, state, zipcode, deadline, weight, notes)
                    if(option == 0):
                        table._insert(pid, package)
                    else:
                        table.append(package)
                
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
        if np.isnan(distance): distance = distance_map [id2][id1]

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
    def route(truck, hashtable, distance_map, packages_info):
        
        priority_package = []  # packages with a deadline before EOD
        regular_package = []  # packages with a delivery deadline of EOD

        # Separate packages with deadlines from packages without deadlines
        for bucket in hashtable.table:
            if len(bucket) == 0: 
                continue
            i = bucket[0][0] #???
            package = hashtable._get(i)

            if package.deadline == 'EOD':
                regular_package.append(package)
            else:
                priority_package.append(package)

        truck.shipments.clear()
        total_distance = 0.00

        def deliver(packages):
            if len(packages) == 0:
                return
            
            nonlocal total_distance
            while len(packages) > 0 and truck.cargo < truck.max_load:
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

                        packages_info[next_package.pid - 1].departure_time = truck.current_time
                        packages_info[next_package.pid - 1].load_time = truck.departure_time
                        packages_info[next_package.pid - 1].which_truck = truck.id

                else:
                    return truck, total_distance

                # Mark the package as on the way, thus removing it from the has
                # htable so its not delivered twice
                next_package.load_time = truck.departure_time

                mileage = Utils.calculate_distance(truck_address, next_address, distance_map)
                delivery_time = truck.current_time + datetime.timedelta(hours=  mileage / truck.velocity)
                print(f"Truck {truck.id} has completed its delivery of package {next_package.pid} to {truck.current_address} and is on it's way to drop off a package at {next_package.address}")
                print(f"Expected arrival time is {delivery_time}\n")

                # Add package to truck and remove from hashtabke
                truck.shipments.append(next_package.pid)
                truck.cargo += 1
                packages.remove(next_package)
                hashtable.delete(next_package.pid)

                if truck.current_address != next_package.address:
                    total_distance += mileage

                # Set new time information
                truck.current_time = delivery_time
                next_package.delivery_time = delivery_time
                packages_info[next_package.pid - 1].delivery_time = delivery_time
                truck.current_address = next_package.address

        deliver(priority_package)
        deliver(regular_package)

        # Record how long the route took in total
        truck.total_distance = total_distance
        return truck, total_distance, hashtable, packages_info

    # Calculates the return time of a truck from its final delivery and returns how far it is
    def calculate_return(truck, truck_address, start_location, distance_map):
        distance = Utils.calculate_distance(truck_address, start_location , distance_map)
        return_time = datetime.timedelta(hours= (distance / truck.velocity))
        print(f'Truck {truck.id} has arrived back at {truck.current_time + return_time} after making {truck.cargo} deliveries')
        truck.current_time = truck.current_time + return_time
        truck.total_distance += distance

        return truck, truck.current_time

    # Used to correct the format of the time input for the UI
    def format_time(time_str):
        time_obj = datetime.strptime(time_str, '%H:%M:%S')
        hour = time_obj.hour
        min = time_obj.minute
        sec = time_obj.second
        temp = timedelta(hours = hour, minutes= min, seconds= sec)
        use_time = datetime(2023, 10, 26, 0, 0, 0, tzinfo=timezone.utc) + temp
        return use_time
