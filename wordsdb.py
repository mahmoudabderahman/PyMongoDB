import pymongo as pm

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
print("inserted_id: ", res.inserted_ids)
