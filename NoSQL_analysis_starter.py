#!/usr/bin/env python
# coding: utf-8

# # Eat Safe, Love

# ## Notebook Set Up

# In[3]:


from pymongo import MongoClient
import pandas as pd
from pprint import pprint


# In[5]:


# Create an instance of MongoClient
mongo = MongoClient(port=27017)


# In[7]:


# assign the uk_food database to a variable name
db = mongo['uk_food']


# In[9]:


# review the collections in our database
print(db.list_collection_names())


# In[11]:


# assign the collection to a variable
establishments = db['establishments']


# ## Part 3: Exploratory Analysis
# Unless otherwise stated, for each question: 
# * Use `count_documents` to display the number of documents contained in the result.
# * Display the first document in the results using `pprint`.
# * Convert the result to a Pandas DataFrame, print the number of rows in the DataFrame, and display the first 10 rows.

# ### 1. Which establishments have a hygiene score equal to 20?

# In[15]:


# Find the establishments with a hygiene score of 20
query = {'scores.Hygiene':20}

# Use count_documents to display the number of documents in the result
print('number of documents in result', establishments.count_documents(query))


# Display the first document in the results using pprint
results = establishments.find(query)
pprint(results[0])


# In[53]:


# Convert the result to a Pandas DataFrame
hygiene_20 = establishments.find(query)
hygiene_df = pd.DataFrame(hygiene_20)
# Display the number of rows in the DataFrame
print('rows in DF', len(hygiene_df))
# Display the first 10 rows of the DataFrame
hygiene_df.head()


# In[57]:


hygiene_df.to_csv('./outputs/hygiene_df.csv', index = False)


# ### 2. Which establishments in London have a `RatingValue` greater than or equal to 4?

# In[20]:


# Find the establishments with London as the Local Authority and has a RatingValue greater than or equal to 4.
query = {'LocalAuthorityName': {'$regex': 'London'}, 'RatingValue': {'$gte': 4}}
print('Number of documents :', establishments.count_documents(query))

# Use count_documents to display the number of documents in the result
print('First result')
results = establishments.find(query)

# Display the first document in the results using pprint
pprint(results[0])


# In[45]:


# Convert the result to a Pandas DataFrame
london_4plus = establishments.find(query)
london_df = pd.DataFrame(london_4plus)

# Display the number of rows in the DataFrame

print('Documents in DF' , len(london_df))

# Display the first 10 rows of the DataFrame
london_df.head(10)



# In[51]:


london_df.to_csv('./outputs/london_rating.csv',index= False)


# ### 3. What are the top 5 establishments with a `RatingValue` rating value of 5, sorted by lowest hygiene score, nearest to the new restaurant added, "Penang Flavours"?

# In[25]:


# Search within 0.01 degree on either side of the latitude and longitude.
# Rating value must equal 5
# Sort by hygiene score

degree_search = 0.01
latitude = 51.4901420
longitude = 0.08384000

query = {'geocode.latitude' : { '$gte' : latitude-degree_search, '$lte' : latitude+degree_search },
        'geocode.longitude' : { '$lte' : longitude-degree_search, '$lte' : longitude+degree_search },
         'RatingValue' : 5
        }
sort =[('sort.Hygiene', 1)]
limit = 5

# Print the results
pprint(list(establishments.find(query).sort(sort).limit(limit)))


# In[41]:


# Convert result to Pandas DataFrame
near_penang_flavours = establishments.find(query).sort(sort).limit(limit)
near_penang_flavours_df = pd.DataFrame(near_penang_flavours)
near_penang_flavours_df

near_penang_flavours_df.to_csv('./outputs/penang_flavours.csv', index = False)


# ### 4. How many establishments in each Local Authority area have a hygiene score of 0?

# In[30]:


# Create a pipeline that:
# 1. Matches establishments with a hygiene score of 0
# 2. Groups the matches by Local Authority
# 3. Sorts the matches from highest to lowest

pipeline = [  {'$match' : {'scores.Hygiene': 0} },
            {'$group' : {'_id': '$LocalAuthorityName', 'count': {'$sum': 1}}},
            {'$sort' : {'count' : -1}
            }]

# Print the number of documents in the result
results = list(establishments.aggregate(pipeline))

# Print the first 10 results
pprint(results[0:10])


# In[62]:


# Convert the result to a Pandas DataFrame
results_df = pd.DataFrame(results)

# Display the number of rows in the DataFrame
print('rows:' , len(results_df))
# Display the first 10 rows of the DataFrame
results_df.head(10)


# In[59]:


results_df.to_csv('aggregate_df.csv',index=False)


# In[ ]:





# In[ ]:




