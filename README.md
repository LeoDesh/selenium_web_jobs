# selenium_web_jobs

selenium_web_jobs is an approach to get jobs data of two main job websites in Austria, where you have to deal with switching sites
and some "Cookies" pop ups. Hence Selenium was chosen instead of beautifulSoup.

## Requirements

The required packages are Selenium and Pandas, which can be installed via: pip install requirements.txt

## Usage

In main.py you can simply execute the script and provide the inputs to get the data.

## Sidenotes

Job_Location has to be a city in Austria and also written in German ('Wien','Salzburg','Klagenfurt')
You can also command out 'jobs_scraping' and use ams_df and karriere_df directly.
Sometimes you have to modify the waiting_seconds to a value between 1.5 and 2.0, depending how fast your website is loaded.

## Procedure for executing main.py
![screenshot](Example_Screenshot.png)
The orange marked words are the example inputs!

## Example Uses of functions: karriere_df, ams_df
karriere_df('Data Science', 'Salzburg', 1.7, 'karriere.csv')
ams_df('Data Science', 'Salzburg', 1.7, 'karriere.csv')

