import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from joblib import dump
data=pd.read_csv('./udemy_courses.csv.xls')
duplicate_rows=data[data.duplicated()]
data1=data.copy()
data1=data1.drop_duplicates()
data1['published_timestamp'] = pd.to_datetime(data1['published_timestamp'])
features = ['course_title', 'level', 'subject']
text_data = data1['course_title'] + ' ' + data1['level'] + ' ' + data1['subject']
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(text_data)
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
# data1.course_title.unique()
def recommend_courses(course_title, cosine_sim=cosine_sim):
    idx = data1[data1['course_title'] == course_title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Exclude the course itself
    course_indices = [i[0] for i in sim_scores]
    recommended_courses = data1[['course_title', 'url', 'price', 'num_subscribers']].iloc[course_indices]

    return recommended_courses.reset_index(drop=True)