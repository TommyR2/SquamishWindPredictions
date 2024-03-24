import pandas as pd
import requests
import xml.etree.ElementTree as ET
import functools as ft
from sqlalchemy import create_engine

xml_dictionary = {"LYTTON A - ": "s0000242_e.xml",
                  "LILLOOET - ": "s0000222_e.xml",
                  "SQUAMISH AIRPORT - ": "s0000323_e.xml",
                  "PEMBERTON AIRPORT (WIND) - ": "s0000173_e.xml",
                  "WEST VANCOUVER AUT - ": "s0000865_e.xml",
                  "MERRITT - ": "s0000006_e.xml",
                  "KAMLOOPS AUT - ": "s0000568_e.xml",
                  "ABBOTSFORD A - ": "s0000758_e.xml",
                  "HOPE A - ": "s0000547_e.xml",
                  "VANCOUVER INTL A - ": "s0000141_e.xml"}

class XMLdata:
    def __init__(self, location):
        xml_code = xml_dictionary[location]
        # Initialize the XML data
        xml_url = f'https://dd.weather.gc.ca/citypage_weather/xml/BC/{xml_code}'
        response = requests.get(xml_url)

        # Make sure data was received
        if response.status_code != 200:
            return
        
        root = ET.fromstring(response.content)
        forecasts = root.findall('.//hourlyForecast')

        if location == "LILLOOET - ":
            # Initialize Data Holders with No wind
            self.Year = []
            self.Month = []
            self.Day = []
            self.Hours = []
            self.Temps = []

            for forecast in forecasts:
                date = forecast.get("dateTimeUTC")
                self.Year.append(int(date[0:4]))
                self.Month.append(int(date[4:6]))
                self.Day.append(int(date[6:8]))
                self.Hours.append(int(date[8:10]))
                self.Temps.append(float(forecast.find('./temperature').text))

            data_dict = {'Year': self.Year,
                         'Month': self.Month,
                         'Day': self.Day,
                         'Hour': self.Hours,
                         location + "Temp (°C)": self.Temps}

            self.df = pd.DataFrame(data_dict)
        else:
            # Initialize Data Holders
            self.Year = []
            self.Month = []
            self.Day = []
            self.Hours = []
            self.Temps = []
            self.Winds = []

            for forecast in forecasts:
                date = forecast.get("dateTimeUTC")
                self.Year.append(int(date[0:4]))
                self.Month.append(int(date[4:6]))
                self.Day.append(int(date[6:8]))
                self.Hours.append(int(date[8:10]))
                self.Temps.append(float(forecast.find('./temperature').text))

                wind_speed = forecast.find('./wind/speed')
                if wind_speed.text == 'Calm':
                    self.Winds.append(float(0))
                else:
                    self.Winds.append(float(forecast.find('./wind/speed').text))
                
            data_dict = {'Year': self.Year,
                         'Month': self.Month,
                         'Day': self.Day,
                         'Hour': self.Hours,
                         location + "Temp (°C)": self.Temps,
                         location + "Wind Spd (km/h)": self.Winds}
            
            self.df = pd.DataFrame(data_dict)

    def getDataFrame(self):
        return self.df


def create_dataFrame():
    dataframes = []

    for key in xml_dictionary.keys():
        preframe = XMLdata(key)
        dataframes.append(preframe.getDataFrame())

    df_final = ft.reduce(lambda left, right: pd.merge(left, right, on=["Year", "Month", "Day", "Hour"]), dataframes)
    return df_final

def connect_dataframe(df):
    host = ''
    user = ''
    password = ''
    database = ''
    table_name = ''

    engine = create_engine(f'mysql://{user}:{password}@{host}/{database}')

    df.to_sql(table_name, con=engine, if_exists='append', index=False, index_label=['Year', 'Month', 'Day', 'Hour'])


def main():
    dataframe = create_dataFrame()
    connect_dataframe(dataframe)
if __name__ == "__main__":
    main()







        

