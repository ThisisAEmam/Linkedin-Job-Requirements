import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('./linkedin_jobs.csv')

def type_label(row):
    if 'Data Scientist' in row['job_title']:
        return 'Data Scientist'
    elif 'Data Analyst' in row['job_title']:
        return 'Data Analyst'
    elif 'Data Engineer' in row['job_title']:
        return 'Data Engineer'
    else:
        return 'Otherwise'

df['job_type'] = df.apply(lambda row: type_label(row), axis=1)
sns.countplot(x= 'job_type', data= df)
plt.xlabel('Job Type')
plt.legend(loc= 'upper right')
plt.show()

