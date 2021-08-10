import os
# import pandas as pd
from linkedin_scraper import get_jobs

chrome_driver_path = os.path.join(os.path.abspath(os.getcwd()), 'chromedriver')

df = get_jobs('Data Scientist', 15, True, chrome_driver_path, 5)

df.to_csv('linkedin_jobs.csv', index= False)

# data = pd.read_csv('https://raw.githubusercontent.com/PlayingNumbers/ds_salary_proj/master/glassdoor_jobs.csv')
# data = data.iloc[:, 1:]
# data.to_csv('glassdoor_jobs.csv', index= False)
