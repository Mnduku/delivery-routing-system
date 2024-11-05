# Delivery Routing System
- Takes in two Excel spreadsheets, one with package information and the other with an address/distance table
- Utilizes the greedy algorithm to implement an efficient delivery route
- Takes into account package deadlines and other possible delivery instructions
- Provides a UI that allows the user to see the status of all packages at any time, and the stats for each truck when the day is done
- Current implementation is with 2 trucks and 3 drivers, modifiable
- Keeps track of the time elapsed and milage traveled for each truck

## Console Output

```console
Please select an option from below
1: Track package/s
2: Truck details
3: Exit

----> 1

Please enter a time in the format (HH:MM:SS)

----> 10:00:00

1: View specific package
2: View all packages?

----> 2
Package #1 was delivered by truck 1 at 2023-10-26 08:37:40+00:00
Package #2 was delivered by truck 1 at 2023-10-26 09:51:00+00:00
Package #3 was delivered by truck 1 at 2023-10-26 08:25:00+00:00
Package #4 was delivered by truck 1 at 2023-10-26 08:25:00+00:00
Package #5 was delivered by truck 1 at 2023-10-26 09:47:20+00:00
Package #6 was loaded into truck 2 at 2023-10-26 08:00:00+00:00 and is currently en route
Package #7 was delivered by truck 1 at 2023-10-26 09:56:20+00:00
Package #8 was loaded into truck 2 at 2023-10-26 08:00:00+00:00 and is currently en route
Package #9 is still at the dock and waiting to be loaded
Package #10 was loaded into truck 2 at 2023-10-26 08:00:00+00:00 and is currently en route
Package #11 was delivered by truck 2 at 2023-10-26 09:07:20+00:00
Package #12 is still at the dock and waiting to be loaded
Package #13 is still at the dock and waiting to be loaded
Package #14 was delivered by truck 1 at 2023-10-26 09:18:40+00:00
Package #15 was delivered by truck 2 at 2023-10-26 08:06:20+00:00
Package #16 was delivered by truck 1 at 2023-10-26 08:13:00+00:00
Package #17 was delivered by truck 1 at 2023-10-26 08:13:00+00:00
Package #18 was delivered by truck 1 at 2023-10-26 09:04:40+00:00
Package #19 was delivered by truck 2 at 2023-10-26 09:18:40+00:00
Package #20 was delivered by truck 1 at 2023-10-26 08:31:20+00:00
Package #21 was delivered by truck 1 at 2023-10-26 08:31:20+00:00
Package #22 was delivered by truck 2 at 2023-10-26 09:51:00+00:00
Package #23 was delivered by truck 2 at 2023-10-26 09:51:00+00:00
Package #24 was delivered by truck 1 at 2023-10-26 08:47:00+00:00
Package #25 is still at the dock and waiting to be loaded
Package #26 was delivered by truck 1 at 2023-10-26 09:26:40+00:00
Package #27 is still at the dock and waiting to be loaded
Package #28 is still at the dock and waiting to be loaded
Package #29 was delivered by truck 1 at 2023-10-26 08:47:00+00:00
Package #30 was delivered by truck 1 at 2023-10-26 09:04:40+00:00
Package #31 was delivered by truck 2 at 2023-10-26 08:04:40+00:00
Package #32 is still at the dock and waiting to be loaded
Package #33 was loaded into truck 1 at 2023-10-26 08:00:00+00:00 and is currently en route
Package #34 was delivered by truck 2 at 2023-10-26 08:13:00+00:00
Package #35 was delivered by truck 2 at 2023-10-26 08:50:40+00:00
Package #36 was delivered by truck 2 at 2023-10-26 08:31:20+00:00
Package #37 was delivered by truck 1 at 2023-10-26 08:47:00+00:00
Package #38 was loaded into truck 2 at 2023-10-26 08:00:00+00:00 and is currently en route
Package #39 was delivered by truck 1 at 2023-10-26 09:04:40+00:00
Package #40 was delivered by truck 1 at 2023-10-26 09:47:20+00:00


```console
*+*===============You are now accessing the delivery routing system==================*+*

Please select an option from below
1: Track package/s
2: Truck details
3: Exit

----> 2

Truck statistics

=========TRUCK 1==========
Departure time: 2023-10-26 08:00:00+00:00
Package count: 16
Packages: [14, 15, 16, 34, 20, 19, 1, 29, 30, 13, 31, 17, 40, 4, 21, 33]
Distance travelled: 38.90

=========TRUCK 2==========
Departure time: 2023-10-26 08:00:00+00:00
Package count: 16
Packages: [37, 38, 3, 36, 18, 23, 11, 24, 26, 22, 2, 7, 10, 5, 8, 39]
Distance travelled: 55.60

=========TRUCK 3==========
Departure time: 2023-10-26 09:40:00+00:00
Package count: 8
Packages: [25, 28, 32, 6, 35, 27, 9, 12]
Distance travelled: 34.60

Total distance: 129.10


```
