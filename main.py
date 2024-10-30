# Created by: Michael Nduku
# Student ID: 004636371
# Date created: 10/24/2024
# WGU UPS Algorithm Project

from utils import Utils
import datetime as dat
from datetime import datetime
from truck import Truck
from datetime import timezone

if __name__ == "__main__":

    # Modifiable variables for different scenarios
    package_file = 'WGUPS Package File.xlsx'
    distance_file = 'WGUPS Distance Table.xlsx'
    total_trucks = 3  # There cant be more then one extra driver with my implementation
    max_drivers = 2
    max_truck_load = 16
    truck_speed = 18
    start_time =  datetime(2023, 10, 26, 8, 0, 0, tzinfo=timezone.utc)
    start_location = '4001 South 700 East'
    truck_fleet = []

    # Console Ouput
    print("*+*===============You are now acessing the delivery routing system=====================*+*")
    print("Please select an option from below")
    print("1: Track package")
    print("2: Delivery details")
    print("3: Exit")

    # Load package data from file
    packages = Utils.filltable(package_file)
    print(packages.show())

    # Load distance + address data from file
    distance_map = Utils.filldistances(distance_file)

    # Instantiate trucks and call the calcualte_route function on them. Last truck is left unchanged
    # We return their return times in order to see when the third truck will be able to operate
    TOTAL_DISTANCE = 0.0
    earliest_return = datetime(2023, 10, 26, 8, 0, 0, tzinfo=timezone.utc) + dat.timedelta(hours= 100)
    
    for i in range(0, total_trucks - (max_drivers - total_trucks + 2)):
        truck_fleet.append(Truck(i, max_truck_load, truck_speed, None, [] , 0.0, start_time, start_time, start_location))

        # Calculate routes and return distances
        truck_fleet[i], distance = Utils.route(truck_fleet[i], packages, distance_map)
        TOTAL_DISTANCE += distance
        truck_fleet[i], return_trip = Utils.calculate_return(truck_fleet[i], truck_fleet[i].current_address, start_location, distance_map)
        if return_trip <= earliest_return: earliest_return = return_trip
    

    # Determine final truck route and return time
    last_truck = (Truck(i, max_truck_load, truck_speed, None, [] , 0.0, earliest_return , earliest_return, start_location))
    last_truck, distance = Utils.route(last_truck, packages, distance_map)
    last_truck, return_trip = Utils.calculate_return(last_truck, last_truck.current_address, start_location, distance_map)
























    
    '''
    total_distance = distance1 + distance2 + distance3

        while True:
            user_input = (input("Your choice: "))

            if user_input == "1":
                # Option 1 implementation
                time_str = input("Please enter a time (HH:MM:SS): ")
                try:
                    time_obj = datetime.datetime.strptime(time_str, '%H:%M:%S')
                    package_option = input("Do you want to view 1) Specific package 2) All packages? ")

                    if package_option == '2':
                        first_package = True  # Flag to track the first package
                        for bucket in ht.table:
                            for package_id, package in bucket:
                                if not first_package:
                                    print()  # Print an empty line between packages
                                else:
                                    first_package = False
                                print(get_delivery_details(package))
                                print("Status at {}: {}".format(time_obj.time(),
                                                                check_package_status(ht, package_id, time_obj)))

                    elif package_option == '1':
                        package_id = int(input("Please enter a package id: "))
                        package = ht.get(package_id)
                        if package:
                            print(get_delivery_details(package))
                            print(
                                "Status at {}: {}".format(time_obj.time(), check_package_status(ht, package_id, time_obj)))
                        else:
                            print("Package not found.")
                    else:
                        print("Invalid option")
                except ValueError:
                    print("Invalid time format. Please enter a valid time (HH:MM:SS).")

            elif user_input == "2":
                for vehicle in [vehicle1, vehicle2, vehicle3]:
                    print(f"Vehicle {vehicle.id} shipments: {vehicle.shipments}")
                    print(f"Vehicle {vehicle.id} ending time: {vehicle.current_time}")
                    print(f"Vehicle {vehicle.id} total distance: {vehicle.total_distance}")
                print(f"Total distance traveled: {round(total_distance, 1)}")

            elif user_input == "3":
                print("Closing the program.")
                break  # Exit the loop and end the program

            else:
                print("Invalid option. Please choose a number between 1 and 3.")

        print("Thank you for using the delivery routing system.")

    '''
