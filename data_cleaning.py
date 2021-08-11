import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import string
from collections import Counter
from itertools import combinations
import math
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv('./linkedin_jobs.csv')

def find_titles_keyword(types):
    titles = []
    for t, i in types:
        titles.append(t)
    substrs = lambda x: {x[i:i+j] for i in range(len(x)) for j in range(len(x) - i + 1)}
    s = substrs(titles[0])
    for val in titles[1:]:
      s.intersection_update(substrs(val))
    return max(s, key=len)

def determine_job_type(df, threshold= 0.7):
    job_titles = df['job_title'].values
    titles_vectors = CountVectorizer().fit_transform(job_titles).toarray()
    titles_cosine = cosine_similarity(titles_vectors)
    types = []
    to_be_skipped = []
    for i, cos_vec in enumerate(titles_cosine):
        one_type = []
        if i in to_be_skipped:
            to_be_skipped.pop(to_be_skipped.index(i))
            continue
        for j, cos_item in enumerate(cos_vec):
            if titles_cosine[i, j] > threshold:
                one_type.append((job_titles[j], j))
                to_be_skipped.append(j)
        
        types.append((one_type, find_titles_keyword(one_type)))
    df['job_type'] = None
    for t in types:
        for x in t[0]:
            if df.loc[x[1]]['job_type'] == None:
                df.loc[x[1]]['job_type'] = t[1]
    return df

df = determine_job_type(df, 0.7)
sns.countplot(x= 'job_type', data= df)
plt.xlabel('Job Type')
plt.xticks(rotation= 60)
# plt.legend(loc= 'upper right')
plt.show()

