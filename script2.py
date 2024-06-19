path =''
import pandas  as pd #Data manipulation
import numpy as np #Data manipulation
import matplotlib.pyplot as plt # Visualization
import seaborn as sns #Visualization

for a in range (1, 13) : 
    df = pd.read_csv('./archive/itineraries.csv', sep=',', nrows=a*1000000)
    df.head()

    print("imported data")


    def_new = pd.DataFrame()

    def extact_month_and_day_from_string(date):
        date = date.split('-')
        return date[1] + '-' + date[2] 

    def extract_first_airname(airline):
        return airline.split('||')[0]

    def weekday(date): 
        return pd.to_datetime(date).weekday()

    def_new["weekday"] = df["flightDate"].apply(weekday)
    def_new["flightDate"] = df["flightDate"].apply(extact_month_and_day_from_string)
    print(len(def_new["flightDate"]), len(df["flightDate"]))

    print('flightDate done')

    def_new["startingAirport"] = df["startingAirport"]
    def_new["destinationAirport"] = df["destinationAirport"]

    """ Create a correspondance between the airport code and an id in a dic object"""
    airports = df['startingAirport'].unique()
    airports = np.sort(airports)
    airports = airports.tolist()
    airports_dict = dict()
    for i in range(len(airports)):
        airports_dict[airports[i]] = i
    print(airports_dict)


    def_new["totalFare"] = df["totalFare"]
    def_new["segmentsAirlineName"] = df["segmentsAirlineName"].apply(extract_first_airname)
    def_new["segmentsEquipmentDescription"] = df["segmentsEquipmentDescription"]

    print(" Done with the data extraction")

    """ Create a correspondance between the airline name and an id in a dic object"""
    airline_name = df['segmentsAirlineName'].unique()
    airline_name = np.sort(airline_name)
    airline_name = airline_name.tolist()
    airline_name_dict = dict()
    for i in range(len(airline_name)):
        airline_name_dict[airline_name[i]] = i
    print(airline_name_dict)

    """ Create a new csv file with the new data"""
    def_new.to_csv('itineraries_new' + str(a) +'.csv', index=False)

""" Extract every possible airport  to start from
start_airports = df['startingAirport'].unique()
print(start_airports)
print(len(start_airports))



Extract all the plane models
plane_models = df['segmentsEquipmentDescription'].unique()
print(plane_models)
print(len(plane_models)) """
