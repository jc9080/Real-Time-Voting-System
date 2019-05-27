#!/usr/bin/env python
# coding: utf-8

# # MongoDB Client

# In[1]:


from pymongo import MongoClient


# In[7]:


# From command line:

# $ mongo
# > use BALLOT_DB


# In[2]:


# Establish a connection to MongoDB
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.BALLOT_DB
ballot_collection = db.ballots


# # Establish consumer relationship with Kafka server

# In[3]:


from kafka import KafkaConsumer
import json


# In[4]:


# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('unverified-votes',
                         group_id='ballots',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer = lambda m: json.loads(m.decode('ascii')))

for ballot in consumer:
    print(ballot)
    ballot_collection.insert_one(ballot.value)
    print("Ballot added to database.")


# In[ ]:





# In[ ]:


# db.ballots.insert_one(
#     {"item": "canvas",
#      "qty": 100,
#      "tags": ["cotton"],
#      "size": {"h": 28, "w": 35.5, "uom": "cm"}})


# In[ ]:


# cursor = db.ballots.find_one({"item": "canvas"})


# In[ ]:


# print(cursor)


# In[ ]:




