import pymongo as pm
import datetime
fh = open("Vocabulary_set.csv", "r") # open the csv file
wd_list = fh.readlines() # read all text at once

wd_list.pop(0) # remove the first line, which contains the header

vocab_list = []

for rawstring in wd_list:
    # store the first word before comma as word, what comes after 
    # the first comma as definition
    word, definition = rawstring.split(',', 1) 
    definition = definition.rstrip() # rstrip to remove any white space
    vocab_list.append({'word':word, 'definition':definition})

#print(vocab_list)

# make connection and create a database
client = pm.MongoClient("mongodb://localhost:27017/")
db = client["vocab"]


vocab_col = db["vocab_list"]
vocab_dict = {'word':'cryptic', 'definition':'secret with hidden meaning'}
res = vocab_col.insert_one(vocab_dict)
print("inserted_id: ", res.inserted_id)
dbs = client.list_database_names()
if "vocab" in dbs:
    print("Database exists")
res = vocab_col.insert_many(vocab_list)
#print("inserted_id: ", res.inserted_ids)
data = vocab_col.find_one()
print(data)

# print all data from the mongodb with the "_id" and "definition"
# excluded
for data in vocab_col.find({}, {"_id":0, "definition":0}):
    print(data)

# find the information for the word 'boisterous'
data = vocab_col.find_one({'word':'boisterous'})
print(data)

# update the definition for the word "boisterous"
upd = vocab_col.update_one({'word': 'boisterous'}, 
{"$set" : {'definition': 'rowdy; noisy'}})
print("modified count: ", upd.modified_count)

# find the information for the word 'boisterous' after updating it
data = vocab_col.find_one({'word':'boisterous'})
print(data)

upd = vocab_col.update_many({}, {"$set" : {"last_updated UTC:":
datetime.datetime.utcnow().strftime('%Y-%m-%d%H%M%SZ')}})
print("modified count: ", upd.modified_count)
