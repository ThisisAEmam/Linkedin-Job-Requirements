import os
from linkedin_scraper import get_jobs

chrome_driver_path = os.path.join(os.path.abspath(os.getcwd()), 'chromedriver')

df = get_jobs('Data Scientist', 40, False, chrome_driver_path)

df.to_csv('linkedin_jobs.csv', index= False)


