import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import get_job_type

df = pd.read_csv('./linkedin_jobs.csv')

df = get_job_type(df, 0.6)

sns.countplot(y= 'type', data= df)
plt.ylabel('Job Type')
plt.show()

