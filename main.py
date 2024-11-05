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

    print(packages.show())

    # Load distance + address data from file
    distance_map = Utils.filldistances(distance_file)

    # Instantiate trucks and call the calcualte_route function on them. Last truck is left unchanged
    # We return their return times in order to see when the third truck will be able to operate
    TOTAL_DISTANCE = 0.0
    earliest_return = datetime(2023, 10, 26, 8, 0, 0, tzinfo=timezone.utc) + dat.timedelta(hours= 100)
    
    for i in range(0, total_trucks - (max_drivers - total_trucks + 2)):
        truck_fleet.append(Truck(i + 1, max_truck_load, truck_speed, 0, [] , 0.0, start_time, start_time, start_location))

        # Calculate routes and return distances
        truck_fleet[i], distance, packages, packages_info = Utils.route(truck_fleet[i], packages, distance_map, packages_info)
        TOTAL_DISTANCE += distance
        truck_fleet[i], return_trip = Utils.calculate_return(truck_fleet[i], truck_fleet[i].current_address, start_location, distance_map)
        if return_trip <= earliest_return: earliest_return = return_trip
    

    # Determine final truck route and return time after first truck return
    last_truck = (Truck(total_trucks, max_truck_load, truck_speed, 0, [], 0.0, earliest_return , earliest_return, start_location))
    truck_fleet.append(last_truck)
    last_truck, distance, packages, packages_info = Utils.route(last_truck, packages, distance_map, packages_info)
    last_truck, return_trip = Utils.calculate_return(last_truck, last_truck.current_address, start_location, distance_map)

    # Console Ouput
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n*+*===============You are now acessing the delivery routing system=====================*+*\n")
    print("Please select an option from below")
    print("1: Track package/s")
    print("2: Delivery details")
    print("3: Exit")

    while True:
        # User interface
        input = (input("\n----> "))
        if input == "1":
            del(input)
            time_str = input("\nPlease enter a time in the format (HH:MM:SS)\n\n----> ")

            try:
                # Parse input time string and add to the base day so we can compare to dates in packages variables
                time = Utils.format_time()
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
            time_str = input("\nPlease enter a time in the format (HH:MM:SS)\n\n----> ")

            try:
                # Parse input time string and add to the base day so we can compare to dates in packages variables
                time = Utils.format_time()
                print(f"\n\nTruck statistics at {time}")
                total_distance = 0.0
                for truck in [truck_fleet]:
                truck.showdata()
                    total_distance += truck.total_distance
                print(f"Total distance: {total_distance}")

            except ValueError:
                    print("Invalid time input. Please enter a time with the format (HH:MM:SS).")
                    break
            
        elif input == "2":
            print("\n\nTruck statistics at")
            total_distance = 0.0
            for truck in [truck_fleet]:
                truck.showdata()
                total_distance += truck.total_distance
            print(f"Total distance: {total_distance}")

        elif input == "3":
                    print("Terminating delivery service. Have a great day !")
                    break
        '''
        else:
            print("Invalid input. Please select a number between 1 and 3.")
            break























    
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
