# Created by: Michael Nduku
# Student ID: 004636371
# Date created: 10/24/2024
# WGU UPS Algorithm Project

from utils import Utils
import datetime as dat
from datetime import datetime, timedelta
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
    start_time = datetime(2023, 10, 26, 8, 0, 0, tzinfo=timezone.utc)
    start_location = '4001 S 700 E'
    truck_fleet = []
    

    # Hash table used to check what packages have and have not been delivered
    packages = Utils.filltable(package_file, 0)

    # List use solely for information holding since packages in hashtable will be removed and thus inacessible
    packages_info = Utils.filltable(package_file, 1)

    # Packages that need to be together based on program notes
    required_packages = [
         [packages._get(14), packages._get(15), packages._get(16), packages._get(19), packages._get(20)],
         [packages._get(36), packages._get(38), packages._get(18), packages._get(3)], 
         [packages._get(32), packages._get(28), packages._get(25), packages._get(6), packages._get(9)]
    ]

    print(packages.show())

    # Load distance + address data from file
    distance_map = Utils.filldistances(distance_file)

    # Instantiate trucks and call the calcualte_route function on them. Last truck is left unchanged
    # We return their return times in order to see when the third truck will be able to operate
 
    earliest_return = datetime(2023, 10, 26, 8, 0, 0, tzinfo=timezone.utc) + dat.timedelta(hours= 100)
    
    for i in range(0, total_trucks - (max_drivers - total_trucks + 2)):
        truck_fleet.append(Truck(i + 1, max_truck_load, truck_speed, 0, [] , 0.0, start_time, start_time, start_location, required_packages[i]))

        # Calculate routes and return distances
        truck_fleet[i], distance, packages, packages_info = Utils.route(truck_fleet[i], packages, distance_map, packages_info)
        truck_fleet[i], return_trip = Utils.calculate_return(truck_fleet[i], truck_fleet[i].current_address, start_location, distance_map)
        if return_trip <= earliest_return: earliest_return = return_trip
    

    # Determine final truck route and return time after first truck return
    last_truck = (Truck(total_trucks, max_truck_load, truck_speed, 0, [], 0.0, earliest_return , earliest_return, start_location, required_packages[total_trucks - 1]))
    truck_fleet.append(last_truck)
    last_truck, distance, packages, packages_info = Utils.route(last_truck, packages, distance_map, packages_info)
    last_truck, return_trip = Utils.calculate_return(last_truck, last_truck.current_address, start_location, distance_map)

    # Console Ouput
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n*+*===============You are now acessing the delivery routing system=====================*+*\n")
    print("Please select an option from below")
    print("1: Track package/s")
    print("2: Truck details")
    print("3: Exit")

    while True:
        # User interface
        input = (input("\n----> "))
        if input == "1":
            del(input)
            time_str = input("\nPlease enter a time in the format (HH:MM:SS)\n\n----> ")

            try:
                # Parse input time string and add to the base day so we can compare to dates in packages variables
                time = Utils.format_time(time_str)
                option = input("\n1: View specific package\n2: View all packages?\n\n----> ")

                if option == '2':
                    # Iterates through entire delivered package table to get all of their statuses
                    for package in packages_info:
                        print(package.return_status(time))
                    break
                    
                elif option == '1':
                    # Finds and prints out the tracking info for the selected package
                    which_package = input("\nEnter the id of the package you want to track\n\n----> ")
                    int_input = int(which_package)
                    print('\n')
                    print(packages_info[int_input - 1].return_status(time))
                    break
                else:
                    print("Invalid input")
                    break

            except ValueError:
                    print("Invalid time input. Please enter a time with the format (HH:MM:SS).")
                    break
            
        elif input == "2":   

                # Prints the stats for each truck at the end of the day
                print(f"\n\nTruck statistics")
                total_distance = 0.0
                for truck in truck_fleet:
                    truck.showdata()
                    total_distance += truck.distance_travelled
                print(f"\nTotal distance: {total_distance:.2f}\n\n\n\n\n\n\n\n\n\n\n\n\n")
                break


        elif input == "3":
                    print("Terminating delivery service. Have a great day !")
                    break
        else:
            print("Invalid input. Please select a number between 1 and 3.")
            break