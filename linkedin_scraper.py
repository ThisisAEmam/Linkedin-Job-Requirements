from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
import math

def get_jobs(keyword, num_jobs, verbose, path):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/brave-browser'
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')
    
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1920, 1080)

    url = 'https://www.linkedin.com/jobs/search/?keywords=' + keyword.replace(' ', '%20') + '&location=Egypt'
    driver.get(url)
    
    # signin_btn = driver.find_element_by_class_name('nav__button-secondary')
    # signin_btn.click()
    
    num_scrolls = math.ceil(num_jobs / 25)
    for i in range(num_scrolls - 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    job_buttons = driver.find_elements_by_class_name("base-card__full-link")[:num_jobs]

    jobs = []

    for job_button in job_buttons:
        print("Jobs collected: {}".format("" + str(len(jobs) + 1) + "/" + str(num_jobs)))

        job_button.click()
        time.sleep(1)
        collected_successfully = False
        
        job_link = job_button.get_attribute('href')
        job_link = job_link[:job_link.find('?')]
        
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
                time.sleep(3)



        #Printing for debugging
        if verbose:
            print("Company Name: {}".format(company_name))
            print("Job Title: {}".format(job_title))
            print("Job Description: {}".format(job_description[:500]))
            print("Critiria: {}".format(list(map(lambda x: x.text, critiria_list))))
        
        jobs.append({
                'title': job_title,
                'type': '',
                'company_name': company_name,
                'description': job_description,
                'link': job_link,
                'seniority_level': seniority_level,
                'employment_type': employment_type,
                'job_function': job_function,
                'industries': industries            
            })
        time.sleep(1)

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.