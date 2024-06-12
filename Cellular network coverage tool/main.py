import json
import sys
import random
import math

#function to read the json file
def read_file(file):
    try: 
        with open(file, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("File not found. Please enter the correct file name.")
        sys.exit()

#function to display global statistics 
def globalStats(data):
    #total number of base stations
    number_base_stations = len(data['baseStations'])
    print('The total number of base stations:', number_base_stations)

    #total number of antennas
    count = 0
    number_antennas = 0
    for base in data['baseStations']: #loop through the base stations
        number_antennas = len(base['ants'])
        count += number_antennas
    print('The total number of antennas:', count)

    #maxmum, minimum and average number of antennas per base
    max_ants = len(data['baseStations'][0]['ants']) #max antennas is set to the list of antennas of the first base station
    min_ants = len(data['baseStations'][0]['ants']) #min antennas is set to the list of antennas of the first base station
    for base in data['baseStations']:
        if len(base['ants']) > max_ants:
            max_ants = len(base['ants'])
        elif len(base['ants']) < min_ants:
            min_ants = len(base['ants'])
    average_ants = count / number_base_stations #average number of antennas per base (total number of antennas divided by total number of base stations)
    print('The maxmum, minimum and average number of antennas per base:', max_ants, ',', min_ants, ',', average_ants)

    #total number of squares (points) in area that are covered by exactly one antenna
    dict1 = { } #dictionary to store all the points
    dict2 = { } #dictionary to store the non-duplicates
    dict3 = { } #dictionary to store the duplicates
    count1 = 0 #counter used as key in dict1

    for i in range(0, number_base_stations):
        for j in range(0, len(data['baseStations'][i]['ants'])):
            for k in range(0, len(data['baseStations'][i]['ants'][j]['pts'])):
                dict1.update({count1: [data['baseStations'][i]['ants'][j]['pts'][k][0], data['baseStations'][i]['ants'][j]['pts'][k][1]]})
                count1 += 1

    #find the duplicates in dictionary
    for i in range(len(dict1)):
        notDuplicate = False
        if i in dict1:
            for j in range(i, len(dict1) - 1):
                if (j+1) in dict1:
                    if dict1[i] == dict1[j+1]:
                        dict3.update({i: dict1.pop(j+1)}) #remove the duplicate from dict 1 and add it to dict3
                        notDuplicate = True
            if notDuplicate == False:
                dict2.update({i: dict1[i]})

    print('The total number of squares (points) in area that are covered by exactly one antenna:', len(dict2))
    
    #total number of squares (points) in area that are covered by more than one antenna
    print('The total number of squares (points) in area that are covered by more than one antenna:', len(dict3))

    #total number of squares (points) in area that are not covered by any antenna
    total_squares = 0
    min_lat = data["min_lat"]
    max_lat = data["max_lat"]
    min_lon = data["min_lon"]
    max_lon = data["max_lon"]
    step = data["step"]

    while min_lat <= max_lat:
        min_lon = data["min_lon"] #reset min_lon to the initial value
        while min_lon <= max_lon:
            if [min_lat, min_lon] not in dict1.values():
                total_squares += 1
            min_lon = round(min_lon + step, 2)
        min_lat = round(min_lat + step, 2)
    print('The total number of squares (points) in area that are not covered by any antenna:', total_squares)

    #maximum number of antennas that cover one square (point)
    max_ants_covering = 0
    for u in range(len(dict3)):
        count = 0
        for i in range(0, number_base_stations):
            for j in range(0, len(data['baseStations'][i]['ants'])):
                for k in range(0, len(data['baseStations'][i]['ants'][j]['pts'])):
                    if u in dict3:
                        if dict3[u] == [data['baseStations'][i]['ants'][j]['pts'][k][0], data['baseStations'][i]['ants'][j]['pts'][k][1]]:
                            count += 1
                            break #once the point is found in the coverage of an antenna, break the loop and go to the next antenna
        if count > max_ants_covering:
            max_ants_covering = count
    print('The maximum number of antennas that cover one square (point):', max_ants_covering)    

    #average number of antennas covering a square (point)
    total_number_of_points = 0
    points_covered_by_at_least_1_antenna = len(dict1) #total number of points covered by at least one antenna (without duplicates)
    average_ants_covering = 0
    for i in range(0, number_base_stations):
        for j in range(0, len(data['baseStations'][i]['ants'])):
            total_number_of_points += len(data['baseStations'][i]['ants'][j]['pts']) #total number of points covered in the area
    average_ants_covering = total_number_of_points / points_covered_by_at_least_1_antenna
    print('The average number of antennas covering a square (point):', round(average_ants_covering, 2))

    #percentage of the covered area by the provider
    total_number_of_points = total_squares + len(dict1) #total number of points in the area
    percentage_covered = (points_covered_by_at_least_1_antenna / total_number_of_points) * 100
    print("The percentage of the covered area = 100 x",points_covered_by_at_least_1_antenna,'/',total_number_of_points, '=', round(percentage_covered,2), '%')  
   
   #id of the antenna and base station covering the maximum number of squares (points)
    max_number_of_squares = 0
    antenna_id = 0
    base_station_id = 0
    for i in range(0, number_base_stations):
        for j in range(0, len(data['baseStations'][i]['ants'])):
            if len(data['baseStations'][i]['ants'][j]['pts']) > max_number_of_squares:
                max_number_of_squares = len(data['baseStations'][i]['ants'][j]['pts'])
                antenna_id = data['baseStations'][i]['ants'][j]['id']
                base_station_id = data['baseStations'][i]['id']
    print("The id of the antenna and base station covering the maximum number of squares (points): base station", base_station_id, ', antenna', antenna_id)



#function to display base station statistics
def baseStationStats(data, n):
    #total number of antennas in the base station
    index = n - 1
    number_antennas = len(data['baseStations'][index]['ants'])
    print('The total number of antennas in the base station', n, ':', number_antennas)

    #total number of squares (points) in area that are covered by exactly one antenna
    dict1 = { } #dictionary to store all the points
    dict2 = { } #dictionary to store the non-duplicates
    dict3 = { } #dictionary to store the duplicates
    count1 = 0 #counter used as key in dict1
    for i in range(0, len(data['baseStations'][index]['ants'])): #loop through the antennas of the base station
        for j in range (0, len(data['baseStations'][index]['ants'][i]['pts'])): #loop through the points of each antenna of that base station
            dict1.update({count1: [data['baseStations'][index]['ants'][i]['pts'][j][0], data['baseStations'][index]['ants'][i]['pts'][j][1]]})
            count1 += 1

    #find the dupllicates in dictionary
    if number_antennas == 1: #if there is only one antenna in the base station then all the points are covered by exactly one antenna
        print('The total number of squares (points) in area that are covered by exactly one antenna:', len(dict1)) 
    else:
        for i in range(len(dict1)):
            notDuplicate = False
            if i in dict1:
                for j in range (i, len(dict1) - 1):
                    if (j+1) in dict1:
                        if dict1[i] == dict1[j+1]:
                            dict3.update({i: dict1.pop(j+1)}) #remove the duplicate from dict 1 and add it to dict3
                            notDuplicate = True
                if notDuplicate == False:
                    dict2.update({i: dict1[i]}) #add the non-duplicate to dict2
        print('The total number of squares (points) in area that are covered by exactly one antenna:', len(dict2))

    #total number of squares (points) in area that are covered by more than one antenna
    print('The total number of squares (points) in area that are covered by more than one antenna:', len(dict3))

    #total number of squares (points) in area that are not covered by any antenna
    total_squares = 0
    min_lat = data["min_lat"]
    max_lat = data["max_lat"]
    min_lon = data["min_lon"]
    max_lon = data["max_lon"]
    step = data["step"]
    while min_lat <= max_lat:
        min_lon = data["min_lon"]
        while min_lon <= max_lon:
            if [min_lat, min_lon] not in dict1.values():
                total_squares += 1
            min_lon = round(min_lon + step, 2)
        min_lat = round(min_lat + step, 2)
    print('The total number of squares (points) in area that are not covered by any antenna:', total_squares)

    #maximum number of antennas that cover one square (point)
    max_ants_covering = 0
    count = 0
    if len(dict3) == 0: #if there are no points covered by more than one antenna, then the maximum number of antennas covering one square is 1
        max_ants_covering = 1
    for u in range(len(dict3)): #for each duplicated point, check the number of antennas covering it
        count = 0
        for i in range(0, len(data['baseStations'][index]['ants'])): #loop through the antennas of the base station
            for j in range(0, len(data['baseStations'][index]['ants'][i]['pts'])): #loop through the points of each antenna
                if u in dict3:
                    if dict3[u] == [data['baseStations'][index]['ants'][i]['pts'][j][0], data['baseStations'][index]['ants'][i]['pts'][j][1]]: #compare the duplicated point with the points of the antennas
                        #if the point is found in the coverage of an antenna, increment the counter and break the loop to go to the next antenna
                        count += 1
                        break
        if count > max_ants_covering:
            max_ants_covering = count

    print('The maximum number of antennas that cover one square (point):', max_ants_covering)

    #average number of antennas covering a square (point)
    total_number_of_points = 0
    points_covered_by_at_least_1_antenna = len(dict1) #total number of points covered by at least one antenna (without duplicates)
    average_ants_covering = 0
    for i in range(0, len(data['baseStations'][index]['ants'])): #loop through the antennas of the base station
        total_number_of_points += len(data['baseStations'][index]['ants'][i]['pts']) #total number of points covered in the area
    average_ants_covering = total_number_of_points / points_covered_by_at_least_1_antenna
    print('The average number of antennas covering a square (point):', round(average_ants_covering, 2))


    #percentage of the covered area by the provider
    total_number_of_points = total_squares + len(dict1) #total number of points in the area (covered and not covered)
    percentage_covered = (points_covered_by_at_least_1_antenna / total_number_of_points) * 100
    print("The percentage of the covered area = 100 x",points_covered_by_at_least_1_antenna,'/',total_number_of_points, '=', round(percentage_covered,2), '%')


    #id of the antenna and base station covering the maximum number of squares (points)
    max_number_of_squares = 0
    antenna_id = 0
    base_station_id = 0
    for i in range(0, len(data['baseStations'][index]['ants'])): #loop through the antennas of the base station
        if len(data['baseStations'][index]['ants'][i]['pts']) > max_number_of_squares:
            max_number_of_squares = len(data['baseStations'][index]['ants'][i]['pts'])
            antenna_id = data['baseStations'][index]['ants'][i]['id']
            base_station_id = data['baseStations'][index]['id']
    print("The id of the antenna and base station covering the maximum number of squares (points): base station", base_station_id, ', antenna', antenna_id)


#function to check coverage
def checkCoverage(data, lat, lon):
    #create a dictionary of all the points
    dict1 = { } #dictionary to store all the points (without duplicates)
    count1 = 0 #counter used as key in dict1
    for i in range(0, len(data['baseStations'])):
        for j in range(0, len(data['baseStations'][i]['ants'])):
            for k in range(0, len(data['baseStations'][i]['ants'][j]['pts'])):
                dict1.update({count1: [data['baseStations'][i]['ants'][j]['pts'][k][0], data['baseStations'][i]['ants'][j]['pts'][k][1]]})
                count1 += 1

    #check if the point is covered by at least one antenna
    dict2 = { } #dictionary to base station and antennas covering the point
    count1 = 0
    if [lat, lon] in dict1.values():
        for i in range(0, len(data['baseStations'])): #loop through the base stations
            for j in range(0, len(data['baseStations'][i]['ants'])): #loop through the antennas of each base station
                for k in range(0, len(data['baseStations'][i]['ants'][j]['pts'])):
                    if [lat,lon] == [data['baseStations'][i]['ants'][j]['pts'][k][0], data['baseStations'][i]['ants'][j]['pts'][k][1]]:
                        dict2.update({count1: ["Base " + str(data['baseStations'][i]['id']), "Antenna " + str(data['baseStations'][i]['ants'][j]['id'])]}) #store the base station and antenna covering the point
                        count1 += 1
                        break #once the point is found in the coverage of an antenna, break the loop and go to the next antenna
        values = dict2.values()
        values_list = list(values) #convert the values to a list to print the values only
        print("The points are convered by at least one antenna. Here are the base stations and antennas covering the point: ", values_list)
    
    #if the points are not explicitly covered by any antenna, choose the nearest antenna
    else:
        entered_coordinates = (lat, lon)
        reference_coordinates = (data['baseStations'][0]['ants'][0]['pts'][0][0], data['baseStations'][0]['ants'][0]['pts'][0][1])
        difference_lat = reference_coordinates[0] - entered_coordinates[0]
        difference_lon = reference_coordinates[1] - entered_coordinates[1]
        distance = math.sqrt(difference_lat**2 + difference_lon**2) #calculate the distance between the entered coordinates and the reference coordinates
        dict2 = {count1: ["Base " + str(data['baseStations'][0]['id']), "Antenna " + str(data['baseStations'][0]['ants'][0]['id'])]} #store the base station and antenna
        for i in range (0, len(data['baseStations'])):
            for j in range (0, len(data['baseStations'][i]['ants'])):
                for k in range (0, len(data['baseStations'][i]['ants'][j]['pts'])):
                    difference_lat = data['baseStations'][i]['ants'][j]['pts'][k][0] - entered_coordinates[0]
                    difference_lon = data['baseStations'][i]['ants'][j]['pts'][k][1] - entered_coordinates[1]
                    current_distance = math.sqrt(difference_lat**2 + difference_lon**2) #calculate the distance between the entered coordinates and the current coordinates
                    if current_distance < distance:
                        distance = current_distance
                        reference_coordinates = (data['baseStations'][i]['ants'][j]['pts'][k][0], data['baseStations'][i]['ants'][j]['pts'][k][1])
                        dict2 = {count1: ["Base " + str(data['baseStations'][i]['id']), "Antenna " + str(data['baseStations'][i]['ants'][j]['id'])]}
                    
        values = dict2.values()
        values_list = list(values)
        print("The points are not convered by any antenna. Here is the base station and antenna covering the nearest point: ", values_list)
        print("the nearest point is:", reference_coordinates)

#main function
def main():
    file = sys.argv[1] #get the file name from the command line
    data = read_file(file)
    choice = 0
    while choice != '4':
        print("1. Display Global Statistic")
        print("2. Display Base Station Statistic")
        print("3. Check Coverage")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            globalStats(data)
        elif choice == '2':
            print("1 Statistics for a random station")
            print("2 Choose a station by Id")
            choice2 = input("Enter your choice: ")
            if choice2 == '1':
                n = random.randint(1, len(data['baseStations']))
                baseStationStats(data, n)
            elif choice2 == '2':
                print("Enter the Id of the station")
                n = input("Enter the Id: ") #n is not an integer but a string
                baseStationStats(data, int(n))  
        elif choice == '3':
            print("Enter the latitude and longitude of the point: ")
            lat = float(input("Latitude: ")) #string
            while lat > data['max_lat'] or lat < data['min_lat']:
                print("Please enter a latitude between", data['min_lat'], "and", data['max_lat'])
                lat = float(input("Latitude: "))
            lon = float(input("Longitude: ")) #string
            while lon > data['max_lon'] or lon < data['min_lon']:
                print("Please enter a longitude between", data['min_lon'], "and", data['max_lon'])
                lon = float(input("Longitude: "))
            checkCoverage(data, lat, lon)
        elif choice == '4':
            print("Thank you for using the program.")
            sys.exit()
        else:
            print("Invalid choice. Please enter again.")
            continue

if __name__ == '__main__':
    main()