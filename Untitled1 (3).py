#!/usr/bin/env python
# coding: utf-8

# In[436]:


# Project ID	Project Name	Project Description	Project Type	Industry	Environmental Impact	Social Responsibility	Governance Practices	Project Location	Project Budget(Millions)	User ID


# In[437]:


# importing libraries
import numpy as np 
import pandas as pd 


# In[438]:


project=pd.read_csv("projects2.csv")


# In[439]:


project.head()


# In[ ]:





# In[440]:


project.shape


# In[441]:


project=project[["project_id","project_name","description","project_type","Industry","location","environment","social","funding_goal(millions_USD)"]]


# In[442]:


project.head()


# In[443]:


#  project['description'] = project['description'].apply(lambda x: x.replace(" ", "") if isinstance(x, str) else x)
project['project_type']


# In[444]:


def collapse(L):
    L1 = []
    for i in L:
        L1.append(i.replace(" ",""))
    return L1


# In[ ]:





# In[445]:


project['location'] =  collapse(project['location'])
project['project_type']=collapse(project['project_type'])
project['Industry']=collapse(project['Industry'])
# # # project['goal']=collapse(project['goal'])


# In[446]:


project['location']


# In[447]:


project['tags'] = project["description"]+" " +project['project_type']+" "+project['Industry']+" "+project["environment"]+" "+project["social"]+ " "  +project['location']+" " +str(project['funding_goal(millions_USD)'])
                                                                                                    


# In[448]:


new = project.drop(columns=["description","project_type","Industry","Industry","environment","social","location","funding_goal(millions_USD)"])
new.head()


# In[449]:


new.head()


# In[450]:


new['tags']


# In[ ]:





# In[451]:


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[452]:


def preprocess_tags(tags):
    processed_tags = []
    for tag in tags:
        processed_tags.append(tag.lower().strip())  # Lowercase and strip each tag
    return processed_tags


# In[453]:


# 2. Apply TF-IDF weighting
vectorizer = TfidfVectorizer(max_features=50000, stop_words='english')
# Preprocess tags if needed
processed_tags = preprocess_tags(new['tags'])  # Apply preprocessing function
vector = vectorizer.fit_transform(processed_tags).toarray()


# In[454]:


# 3. Calculate cosine similarity
similarity = cosine_similarity(vector)


# In[455]:


# Print the shape of the similarity matrix
print(similarity.shape)


# In[461]:


sorted(similarity[0])


# In[457]:


new[new['project_name'] == 'Sustainable Forestry Practices'].index[0]


# In[458]:


def recommend(movie):
    index=new[new['project_name'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        print(new.iloc[i[0]].project_name)
        


# In[459]:


recommend('Green Transportation Initiative')


# In[463]:


import pickle


# In[465]:


pickle.dump(new,open('project_list.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))


# In[466]:


pickle.dump(project,open('details.pkl','wb'))


# In[ ]:




