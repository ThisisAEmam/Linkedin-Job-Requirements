from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/brave-browser'
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1920, 1080)

    url = 'https://www.linkedin.com/jobs/search/?keywords=' + keyword.replace(' ', '%20') + '&location=Egypt'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        
        #Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("base-card__full-link")  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might
            time.sleep(3)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_class_name('topcard__org-name-link').text
                    job_title = driver.find_element_by_class_name('topcard__title').text
                    try:
                        driver.find_element_by_class_name('show-more-less-html__button').click()
                        time.sleep(1)
                    except NoSuchElementException:
                        pass
                    job_description = driver.find_element_by_class_name('show-more-less-html__markup').text
                    seniority_level = None
                    employment_type = None
                    job_function = None
                    industries = None
                    critiria_list = driver.find_elements_by_class_name("description__job-criteria-item")
                    for critiria_item in critiria_list:
                        critiria_type, critiria_text = critiria_item.text.split('\n')
                        if critiria_type == 'Seniority level':
                            seniority_level = critiria_text
                        elif critiria_type == 'Employment type':
                            employment_type = critiria_text
                        elif critiria_type == 'Job function':
                            job_function = critiria_text
                        elif critiria_type == 'Industries':
                            industries = critiria_text
                    collected_successfully = True
                except:
                    time.sleep(5)



            #Printing for debugging
            if verbose:
                print("Company Name: {}".format(company_name))
                print("Job Title: {}".format(job_title))
                print("Job Description: {}".format(job_description[:500]))
                print("Critiria: {}".format(list(map(lambda x: x.text, critiria_list))))
            
            jobs.append({
                    'company_name': company_name,
                    'job_title': job_title,
                    'job_description': job_description,
                    'seniority_level': seniority_level,
                    'employment_type': employment_type,
                    'job_function': job_function,
                    'industries': industries                 
                })
            time.sleep(3)

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.