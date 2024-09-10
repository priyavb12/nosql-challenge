#!/usr/bin/env python
# coding: utf-8

# # Eat Safe, Love

# ## Part 1: Database and Jupyter Notebook Set Up

# Import the data provided in the `establishments.json` file from your Terminal. Name the database `uk_food` and the collection `establishments`.
# 
# Within this markdown cell, copy the line of text you used to import the data from your Terminal. This way, future analysts will be able to repeat your process.
# 
# e.g.: Import the dataset with `YOUR IMPORT TEXT HERE`

# In[1]:


# Import dependencies
from pymongo import MongoClient
from pprint import pprint


# In[3]:


# Create an instance of MongoClient
mongo = MongoClient(port=27017)


# In[5]:


# confirm that our new database was created
print(mongo.list_database_names())


# In[7]:


# assign the uk_food database to a variable name
db = mongo['uk_food']


# In[9]:


# review the collections in our new database
print(db.list_collection_names())


# In[15]:


# review the collections in our new database
print(db.list_collection_names())


# In[21]:


# review a document in the establishments collection
pprint(db.establishments.find_one())


# In[23]:


# assign the collection to a variable
establishments = db['establishments']


#  ## Part 2: Update the Database

# 1. An exciting new halal restaurant just opened in Greenwich, but hasn't been rated yet. The magazine has asked you to include it in your analysis. Add the following restaurant "Penang Flavours" to the database.

# In[27]:


# Create a dictionary for the new restaurant data
new_restaurant = {
    "BusinessName":"Penang Flavours",
    "BusinessType":"Restaurant/Cafe/Canteen",
    "BusinessTypeID":"",
    "AddressLine1":"Penang Flavours",
    "AddressLine2":"146A Plumstead Rd",
    "AddressLine3":"London",
    "AddressLine4":"",
    "PostCode":"SE18 7DY",
    "Phone":"",
    "LocalAuthorityCode":"511",
    "LocalAuthorityName":"Greenwich",
    "LocalAuthorityWebSite":"http://www.royalgreenwich.gov.uk",
    "LocalAuthorityEmailAddress":"health@royalgreenwich.gov.uk",
    "scores":{
        "Hygiene":"",
        "Structural":"",
        "ConfidenceInManagement":""
    },
    "SchemeType":"FHRS",
    "geocode":{
        "longitude":"0.08384000",
        "latitude":"51.49014200"
    },
    "RightToReply":"",
    "Distance":4623.9723280747176,
    "NewRatingPending":True
}


# In[29]:


# Insert the new restaurant into the collection
establishments.insert_one(new_restaurant)


# In[43]:


# Check that the new restaurant was inserted
print(establishments.find_one({'BusinessName' : 'Penang Flavours' }))


# 2. Find the BusinessTypeID for "Restaurant/Cafe/Canteen" and return only the `BusinessTypeID` and `BusinessType` fields.

# In[45]:


# Find the BusinessTypeID for "Restaurant/Cafe/Canteen" 
#and return only the BusinessTypeID and BusinessType fields

query = {'BusinessType' : 'Restaurant/Cafe/Canteen' }
fields = {'BusinessTypeID' :1, 'BusinessType' :1}
pprint(establishments.find_one(query, projection=fields))


# 3. Update the new restaurant with the `BusinessTypeID` you found.

# In[47]:


# Update the new restaurant with the correct BusinessTypeID
establishments.update_one({'BusinessName' : 'Penang Flavours'},
                          {'$set': {'BusinessTypeID': 1}})


# In[49]:


# Confirm that the new restaurant was updated
pprint(establishments.find_one({'BusinessName' : 'Penang Flavours'}))


# 4. The magazine is not interested in any establishments in Dover, so check how many documents contain the Dover Local Authority. Then, remove any establishments within the Dover Local Authority from the database, and check the number of documents to ensure they were deleted.

# In[51]:


# Find how many documents have LocalAuthorityName as "Dover"
dover_documents = establishments.count_documents({'LocalAuthorityName' : 'Dover'})
dover_documents


# In[53]:


# Delete all documents where LocalAuthorityName is "Dover"
establishments.delete_many({'LocalAuthorityName' : 'Dover'})


# In[55]:


# Check if any remaining documents include Dover
dover_documents = establishments.count_documents({'LocalAuthorityName' : 'Dover'})
dover_documents


# In[57]:


# Check that other documents remain with 'find_one'
pprint(establishments.find_one())


# 5. Some of the number values are stored as strings, when they should be stored as numbers.

# Use `update_many` to convert `latitude` and `longitude` to decimal numbers.

# In[61]:


# Change the data type from String to Decimal for longitude and latitude
establishments.update_many({}, [{'$set': {'geocode.latitude': {'$toDouble' : '$geocode.latitude'},
                                 'geocode.longitude': {'$toDouble' : '$geocode.longitude'} }}])


# Use `update_many` to convert `RatingValue` to integer numbers.

# In[63]:


# Set non 1-5 Rating Values to Null
non_ratings = ["AwaitingInspection", "Awaiting Inspection", "AwaitingPublication", "Pass", "Exempt"]
establishments.update_many({"RatingValue": {"$in": non_ratings}}, [ {'$set':{ "RatingValue" : None}} ])


# In[65]:


# Change the data type from String to Integer for RatingValue
establishments.update_many({'RatingValue': {'$type' : 'string'}}, [{'$set':{'RatingValue': {'$toInt': '$RatingValue'}}}])




# In[67]:


# Check that the coordinates and rating value are now numbers
pprint(establishments.find_one())


# In[ ]:




