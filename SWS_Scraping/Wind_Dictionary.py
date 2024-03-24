"""
Usable Dates
2016: May 13 - Sep 18
2017: May 7 - October 15
2018: May 15 - Sep 15
2019: May 14 - Sep 24
2020: May 17 - Sep 29
2021: April 14 - Oct 12
2022: May 23 - Sep 19
2023: May 19 - Sep 23
"""


# Note all months and days minus 1 for 0 index

class WindDictionary:
    """ 
    Holds the indexes for all available dates that contain data.
    This is generally mid-May(4) through mid-September(9).
    """
    def __init__(self, Year):
        self.Year = Year
        
    def getMonths(self):
        self.monthDic = {"2016": [4, 9],
                         "2017": [4,10],
                         "2018": [4, 9],
                         "2019": [4, 9],
                         "2020": [4, 9],
                         "2021": [3, 10],
                         "2022": [4, 9],
                         "2023": [4, 9]}
        start, end = self.monthDic[self.Year][0], self.monthDic[self.Year][1]
        return [str(month) for month in range(start, end)]
    
    def getDays(self, Month):
        dic1 = {"4":[12, 31],
                "5":[0, 30],
                "6":[0, 31],
                "7":[0, 31],
                "8":[0, 18],
                }
        
        dic2 = {"4":[6, 31],
                "5":[0, 30],
                "6":[0, 31],
                "7":[0, 31],
                "8":[0, 30],
                "9":[0,15]
                }

        dic3 = {"4":[14, 31],
                "5":[0, 30],
                "6":[0, 31],
                "7":[0, 31],
                "8":[0, 15],
                }
        
        dic4 = {"4":[13, 31],
                "5":[0, 30],
                "6":[0, 31],
                "7":[0, 31],
                "8":[0, 24],
                }
        
        dic5 = {"4":[16, 31],
                "5":[0, 30],
                "6":[0, 31],
                "7":[0, 31],
                "8":[0, 29],
                }

        dic6 = {"3":[13, 30],
                "4":[0, 31],
                "5":[0, 30],
                "6":[0, 31],
                "7":[0, 31],
                "8":[0, 30],
                "9":[0, 12]
                }

        dic7 = {"4":[22, 31],
                "5":[0, 30],
                "6":[0, 31],
                "7":[0, 31],
                "8":[0, 19],
                }
        
        dic8 = {"4":[18, 31],
                "5":[0, 30],
                "6":[0, 31],
                "7":[0, 31],
                "8":[0, 23],
                }
        
        selectionDic = {"2016": dic1,
                        "2017": dic2,
                        "2018": dic3,
                        "2019": dic4,
                        "2020": dic5,
                        "2021": dic6,
                        "2022": dic7,
                        "2023": dic8,
                        }
        
        currentDictionary = selectionDic[self.Year]
        start, end = currentDictionary[Month][0], currentDictionary[Month][1]
        return [day for day in range(start, end)]