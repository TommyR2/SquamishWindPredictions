from SWS_Scraping import *
from Wind_Dictionary import *
import time


def main():
    # Initialize the SWS Site
    SWS_Site = WebScrape()

    # Select the available years
    Years = [str(Year) for Year in range(2016, 2024)]
    final_dataframes = []
    for Year in Years:
        # Select the usable months and days from the Wind_Dictionary Library
        date_dic = WindDictionary(Year)
        Months = date_dic.getMonths()
        for Month in Months:
            Days = date_dic.getDays(Month)
            for day in Days:   
                SWS_Site.selectDate(Year, Month, day)
                time.sleep(2)

                # Downloading Data                
                final_dataframes.append(SWS_Site.collectData())
                print(f"Day added from {Year} - {Month}", flush = True)
    
    SWS_Site.end()
    complete_dataset = pd.concat(final_dataframes)
    complete_dataset.to_csv(f'SquamishWind.csv', index=False)
    return complete_dataset

if __name__ == "__main__":
    main()
