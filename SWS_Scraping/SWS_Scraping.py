from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.chrome.options import Options
import re
import pandas as pd


class WebScrape:
    """
    Scrapes the datapoints for each day and returns a list of pandas dataframes.
    """
    def __init__(self):
        """
        Sends a request to the SWS Site with the configurations that allow Selenium to
        run in the background.
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://squamishwindsports.com/conditions/wind/")

    def selectDate(self, Year, Month, Day):
        self.Year = Year
        self.Month = Month
        self.Day = Day
        # Opening the Calendar Dropdown menu
        initial_button = self.driver.find_element(By.ID, "datepicker")
        initial_button.click()

        # Selecting the year in the dropdown menu
        year_button = self.driver.find_element(By.CLASS_NAME, "ui-datepicker-year")
        year_select = Select(year_button)
        year_select.select_by_value(Year)

        # Selecting the month in the dropdown menu
        month_button = self.driver.find_element(By.CLASS_NAME, "ui-datepicker-month")
        month_select = Select(month_button)
        month_select.select_by_value(Month)

        # Selecting the day in the dropdown menu
        table = self.driver.find_element(By.CLASS_NAME, "ui-datepicker-calendar")
        days = table.find_elements(By.TAG_NAME, "td")
        usable_days = []
        for day in days:
            # Removing blank days at the beginning of calendar dropdown due to formatting
            if day.text != " ":
                usable_days.append(day)
        
        link = usable_days[int(Day)]
        link.click()

    def collectData(self):
        # Initializing the chart element
        element = self.driver.find_element(By.ID, 'chart')

        # Activating chart by clicking on it
        element.click()

        # Simulate interactions (hover over data points to trigger tooltips)
        data_points = self.driver.find_elements(By.CLASS_NAME, 'highcharts-point')
        action = ActionChains(self.driver)
        
        #Creating a list of Data
        DataFrames = []
        prev_data = None
        for data_point in data_points:
            action.move_to_element(data_point).perform()

        # Extract the text from the tooltips
            tooltip_text = self.driver.execute_script('return document.querySelector(".highcharts-tooltip").textContent;')
            data = Datapoint(tooltip_text)
            # Attaching a date to each Datpoint object
            data.assignDate(self.Year, self.Month, self.Day)

            # Fixing the problem where duplicate datapoints are scraped
            if data.getTime() == prev_data:
                continue
            
            #Creating a DataFrame
            data_dict = {"Year": [data.getDate()[0]],
                         "Month": [data.getDate()[1]],
                         "Day": [data.getDate()[2]],
                         "Time": [data.getTime()],
                         "Lull": [data.getLull()],
                         "Average": [data.getAverage()],
                         "Gust": [data.getGust()],
                         "Direction": [data.getDirection()]}
            
            df = pd.DataFrame(data_dict)
            DataFrames.append(df)

            prev_data = data.getTime()
        final_df = pd.concat(DataFrames)
        return final_df
        
    def end(self):
        self.driver.quit()


class Datapoint:
    """
    Holds an individual datapoint. Datapoints are taken every three minutes
    and contain the current Lull, Average and Gust.
    """
    def __init__(self, raw_text):
        self.raw_text = raw_text

        #Initializing all values to None
        self.average_value = None
        self.gust_value = None
        self.lull_value = None
        self.direction_value = None
        self.time_value = None

        #Parsing Average
        average_parsed = re.search(r'Average: ([0-9.]+)', self.raw_text)
        self.average_value = average_parsed.group(1)

        #Parsing Gusts
        gust_parsed = re.search(r'Gust: ([0-9.]+)', self.raw_text)
        self.gust_value = gust_parsed.group(1)

        #Parsing Lulls
        lull_parsed = re.search(r'Lull: ([0-9.]+)', self.raw_text)
        self.lull_value = lull_parsed.group(1)

        #Parsing Directions
        direction_parsed = re.search(r'Direction \(deg\): (\d+)', self.raw_text)
        self.direction_value = direction_parsed.group(1)

        #Parsing Times
        time_parsed = re.search(r'Time: (.+)', self.raw_text)
        self.time_value = time_parsed.group(1)

    
    def __str__(self):      
        return str(f"Wind Average: {self.average_value}\n"
                f"Wind Gust: {self.gust_value}\n" + 
                f"Wind Lull: {self.lull_value}\n" + 
                f"Wind Direction: {self.direction_value}\n" + 
                f"Time: {self.time_value}\n" + 
                f"Date: {self.Year} - {self.Month} - {self.Day}")

    def getAverage(self):
        return eval(self.average_value)
    
    def getGust(self):
        return eval(self.gust_value)
    
    def getLull(self):
        return eval(self.lull_value)
    
    def getDirection(self):
        return eval(self.direction_value)
    
    def getTime(self):
        return self.time_value
    
    def assignDate(self, Year, Month, Day):
        self.Year = Year
        self.Month = Month
        self.Day = Day

    def getDate(self):
        return [self.Year, self.Month, self.Day]

