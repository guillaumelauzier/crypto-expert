# crypto-expert

----
System architecture
----

![alt text](https://raw.githubusercontent.com/guillaumelauzier/crypto-expert/main/Chantal.drawio.png)



Here is an example of a matching algorithm in Python that matches data between two MongoDB databases using the standard deviation method:

```
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
            
 ```
 The algorithm takes two MongoDB databases, the names of the collections to match, the key to match on, and the threshold for the standard deviation as input. It retrieves all the documents from the first collection and the second collection, then it creates a dictionary to store the standard deviation of the key values. It iterates over the documents in the first collection and calculates the standard deviation of the key values for the documents in the second collection with the same key. If the standard deviation is less than or equal to the threshold, it updates the first document with the data from the second document. If no match is found, it prints a message indicating so.
 
 ------
 What is mongodb partitioning ?
 ------
 MongoDB partitioning, also known as sharding, is a technique used to distribute data across multiple servers to improve scalability and performance. It allows you to split your data horizontally across multiple machines, so that you can store and retrieve large amounts of data without being limited by the storage and processing capabilities of a single machine.

MongoDB uses a shard key to partition the data. The shard key is a field or set of fields that determines which documents belong to which shard. The documents are then distributed across the shards based on the shard key value. Each shard holds a subset of the data, called a shard range, and the shard key values for the documents in that shard range fall within a certain range. This allows for efficient data retrieval based on the shard key value.

There are two main components to MongoDB partitioning:

Shard: a MongoDB instance that holds a subset of the data.
Config Server: a MongoDB instance that holds the metadata for the sharded cluster. This includes information about the shard key range and the location of the data.
MongoDB partitioning can be used with replica sets to provide high availability and failover capabilities. It also allows you to add or remove shards as needed to handle changes in data size and traffic.

Sharding is a powerful feature that allows you to scale MongoDB horizontally. However, it also add complexity to your deployment and require more resources. Before implementing sharding, it is important to consider your specific use case, data size and performance requirements, and the resources available to you.
