import pymongo
import numpy as np

def match_making(db1, db2, collection1, collection2, key, std_dev_threshold):
    """
    Matches data between two MongoDB databases using standard deviation method.
    Parameters:
    - db1: pymongo.database.Database, the first database
    - db2: pymongo.database.Database, the second database
    - collection1: str, the name of the collection in the first database
    - collection2: str, the name of the collection in the second database
    - key: str, the key to match on
    - std_dev_threshold: float, the threshold for the standard deviation
    """
    coll1 = db1[collection1]
    coll2 = db2[collection2]

    # Get all documents from the first collection
    docs1 = coll1.find()

    # Create a dictionary to store the standard deviation of the key values
    std_devs = {}

    # Iterate over the documents in the second collection and calculate the standard deviation of the key values
    for doc2 in coll2.find():
        key_val = doc2[key]
        if key_val in std_devs:
            std_devs[key_val].append(doc2)
        else:
            std_devs[key_val] = [doc2]

    # Iterate over the documents in the first collection
    for doc1 in docs1:
        key_val = doc1[key]
        if key_val in std_devs:
            # Get the list of documents with the same key value
            docs2 = std_devs[key_val]
            # Calculate the standard deviation of the key values
            std_dev = np.std([doc[key] for doc in docs2])
            if std_dev <= std_dev_threshold:
                # If the standard deviation is less than or equal to the threshold, update the first document with the data from the second document
                coll1.update_one({'_id': doc1['_id']}, {'$set': docs2[0]})
                print(f"Matched and updated document with {key}: {key_val}")
            else:
                print(f"No match found for document with {key}: {key_val} (standard deviation: {std_dev})")
        else:
            print(f"No match found for document with {key}: {key_val}")
