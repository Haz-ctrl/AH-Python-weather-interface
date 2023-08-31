#AH Computing project weather class
#Hashim Iqbal

#This file contains two SDD AH constructs, Object-oriented programming and Bubble sorts
#SDD also integrates with Database Design and Development here, through the databaseConnection() method.

#This class will be imported into the main script, which handles UI and other 'front-end' processes.
#This class acts as the 'back-end' of the application, providing validation, requests and database connection.
'''
Dependencies:
    Requests to handle fetch requests to the API.
    Date from Datetime to get today's date
    Dataclass from Dataclasses so that the record structure and array of records can be implemented.
    mySQL connector to establish connection with the database, and run the INSERT query.
    We will also need to pass information from the main script to this one, back and forth.
'''
import requests
import datetime
from dataclasses import dataclass
import mysql.connector

class Weather:

    #The city and url are global variables passed in outside of the class
    def __init__(self):
        #Stores today's date
        self._todaydate = datetime.date.today()
        #Formats it as day of the week day. month year.
        self._longdate = self._todaydate.strftime('%A %d. %B %Y')
        #Formats it as yyyy/mm/dd. This is the only accepted format by mysql.
        self._databasedate = self._todaydate.strftime('%Y/%m/%d')

        #Gets the current time and formats it as hh:mm:ss
        self._time = datetime.datetime.now()
        self._formattime = self._time.strftime("%H:%M:%S")

    #Fetches the data using the requests library, and displays it.
    def fetchData(self, city):

        #Url holds the API being referenced. City name is supposed to be after q =, so the user input will be spliced in there.
        self._url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=b8f9750fa728b7bc552d171f80148d4b&units=metric'.format(city)

        #Makes a fetch request to this API, and tells python to read it as JSON data.
        res = requests.get(self._url)
        data = res.json()

        #Status code
        status = None

        #If the API returns a 404 status code i.e. the city hasn't been found, this conditional statement evaluates as true.
        #The boolean flag evaluates as true which tells our other script that something is wrong.
        #If everything checks out, begin the process of harvesting the data and sending it back.
        if(res.status_code == 404):
            status = False
            return status

        else:
            #Navigates the different branches in the data to define each variable.
            #The country name will be in the 'sys' branch and the attribute country.
            self._country = data['sys']['country']
            #The city name will be on the outer most branch in the name attribute.
            self._city = data['name']
            #Latitude will be in the coord branch and the attribute lat.
            self._lat = data['coord']['lat']
            #Longitude will be in coord branch and the attribute lon.
            self._lon = data['coord']['lon']
            #Temperature will be in the main branch and the attribute temp.
            self._temp = data['main']['temp']
            #Wind Speed will be in the wind branch and the attribute speed.
            self._wind_speed = data['wind']['speed']
            #Description will be in the weather branch, as the first element of the array, and the attribute description.
            self._desc = data['weather'][0]['description']
        
            #The name of the icon, which will be used to sort through various images and display a weather icon on the screen.
            #This is a public variable, as indicated by the lack of underscore.
            self.icon = data['weather'][0]['icon']

            #Return our data as an array which will then be displayed by the GUI
            return [self._country, self._city, self._lat, self._lon, self._temp, self._wind_speed, self._desc]


    #Opens a new .txt file for writing, and writes the same weather info as before.
    #.txt file is named after the city entered, and also has the day's date.
    #Is only invoked if the user selects 'yes' to file writing in the GUI.
    #Otherwise, the method is skipped and readFile() is executed next.
    def writeData(self, filepath):

        #Creates a .txt file, which is of the name the user wrote in the file dialog window.
        with open ('{}'.format(filepath), 'w') as writefile:

            #Writes the city and country abbriveation as a heading
            writefile.write('The weather in {}, {}: '.format(self._city, self._country) + '\n')

            #Writes the date and time of writing just for organisation.
            writefile.write('Date of writing (GMT): {}'.format(self._longdate) + ',' + '\n')
            writefile.write('Time of writing (GMT): {}'.format(self._formattime) + ',' + '\n')

            #Writes latitude, longitude and other weather information.
            writefile.write('Latitude: {}'.format(self._lat) + ',' + '\n')
            writefile.write('Longitude: {}'.format(self._lon) + ',' + '\n')
            writefile.write('Temperature: {} °C'.format(self._temp) + ',' + '\n')
            writefile.write('Wind Speed: {} m/s'.format(self._wind_speed) + ',' + '\n')
            writefile.write('Description: {}'.format(self._desc))


    #Opens the .csv file for reading in 100 city names and country names.
    #These will be stored in an array of records.
    def readFile(self):

        #Declare record structure for each city.
        #This will be the layout of the information in the database.
        @dataclass
        class city():
            city = str
            country = str
            date = str
            temp = 0.0
            wind = 0.0
            desc = str

        #Make an array of records
        self._cities = [city() for counter in range(100)]
        counter = 0

        #Open the cities.csv file for reading.
        with open('cities.csv') as readfile:
            #Read the first line of the file
            line = readfile.readline().rstrip('\n')

            #While there is text on the line
            while line:
                #Split on the comma
                items = line.split(',')

                #Populate record attributes with data from the file
                self._cities[counter].city = items[0]
                self._cities[counter].country = items[1]

                counter += 1
                line = readfile.readline().rstrip('\n')


    #Sorts the records into alphabetical order of city names, by means of a bubble sort.
    #Country names aren't alphabetically sorted.
    def sortCities(self):
        #Conditional loop bubble sort
        swaps = True
        outer = len(self._cities) - 1

        #Only when swaps evaluates as true, the statement satisfies and the loop executes.
        while(swaps):
            swaps = False
            for inner in range(outer):

                #If the current record has a city with first letter further along than the next one's,
                #the statement is satisfied.
                if self._cities[inner].city > self._cities[inner + 1].city:
                    swaps = True

                    #Set up temporary variable
                    temp = self._cities[inner]

                    #Swap the records around
                    self._cities[inner] = self._cities[inner + 1]
                    self._cities[inner + 1] = temp

            #Decrement outer
            outer -= 1


    #Performs a fetch request for each sorted record.
    #Proceeds to populate each record with the date, temperature, wind speed and description.
    def populateRecords(self):

        #Fixed loop that runs for every record in the array, and populates each record by performing a fetch request
        #for each one, and assigns the data accordingly.
        for x in range(len(self._cities)):
            #The date and time attributes will just be the same as the variables we set up earlier in __init__().
            self._cities[x].date = self._databasedate

            #Performs fetch request for each record
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID=b8f9750fa728b7bc552d171f80148d4b&units=metric'.format(self._cities[x].city)
            res = requests.get(url)
            data = res.json()

            #Navigating the fetched data once again to assign values to each record.
            self._cities[x].temp = data['main']['temp']
            self._cities[x].wind = data['wind']['speed']
            self._cities[x].desc = data['weather'][0]['description']


    #Finally establishes a connection with the database.
    #Runs an INSERT query for each record to insert their attributes under the database headings.
    def databaseConnection(self):

        #Connects to the AH_Project database
        try:
            cnx = mysql.connector.connect (
                host = 'localhost',
                database = 'AH_Project',
                user = 'root',
                password = 'root',
                #Mac Only
                unix_socket = '/Applications/MAMP/tmp/mysql/mysql.sock'
            )
        #Display error information if there happens to be one.
        except mysql.connector.Error as err:
            return False

        #If the script connects successfully, run the INSERT query and close connection.
        else:
            print("Successfully connected to database. Connection ID: ", cnx.connection_id)

            cursor = cnx.cursor()

            #Empty out the table of all current records
            #because we want to fill it with nice, up to date information about weather
            #and we don't want cities appearing twice.
            cursor.execute("TRUNCATE TABLE WeatherData")

            #Runs an INSERT query for each record in the array.
            for x in range(len(self._cities)):
                query = "INSERT INTO WeatherData VALUES (%s, %s, %s, %s, %s, %s)"
                data = (self._cities[x].city, self._cities[x].country, self._cities[x].date, self._cities[x].temp, self._cities[x].wind, self._cities[x].desc)

                #Execute the query, passing in the query string and record data as parameters.
                cursor.execute(query, data)

            #Commit changes to the database
            cnx.commit()

            #Close connection
            cursor.close()
            cnx.close()

            return cnx.connection_id