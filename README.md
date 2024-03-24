# Squamish Wind Predictor
Using Python, Selenium and Pandas, scrapes 8 years worth of wind data from the Squamish Windsports society wind meter.
Utilizing the historic temperature and wind data from the Government of Canada's public data set, creates a TensorFlow model to predict
hourly wind speed at the Squamish Spit. 

<img width="668" alt="Screenshot 2024-03-23 at 8 40 25 PM" src="https://github.com/TommyR2/SquamishWindPredictions/assets/115518444/e8ab3a4e-10fd-4252-8ab1-142c9de43a83">
<img width="671" alt="Screenshot 2024-03-23 at 8 58 36 PM" src="https://github.com/TommyR2/SquamishWindPredictions/assets/115518444/f7468eac-df33-496a-9a86-586e89f0715f">
<img width="668" alt="Screenshot 2024-03-23 at 8 58 57 PM" src="https://github.com/TommyR2/SquamishWindPredictions/assets/115518444/b1ac39ba-dc5b-4026-9015-2c7d043515ce">


Can also be set up to predict wind data up to 24 hours into the future. 
Upon configuring a MYSQL database and inserting the set up credentials, writeGovData.py utilizes the Government of Canada's hourly wind predictions
to update the SQL database with expected future temperatures and wind speeds. predictWindData.py can then be run to receive a forecast for the spefified
day's wind.

<img width="992" alt="Screenshot 2024-03-23 at 9 14 08 PM" src="https://github.com/TommyR2/SquamishWindPredictions/assets/115518444/9d4570ff-ea9b-40e9-b53a-1641d8687620">

