import chromadb
import pandas as pd
import numpy as np

# what is happening here?
# 1: read the dataset
# 2: convert to string (that's the format the db expects)
# 3: preferably set the index and then add to the db collection / or start simple
YT_comments = pd.read_csv("../intake/data/YoutubeCommentsDataSet.csv", dtype=str, nrows=100)
YT_comments.dropna(inplace=True)
YT_comments.reset_index(inplace=True)
print(YT_comments.dtypes)


documents = YT_comments['Comment'].tolist()
print(len(documents))
metadata = []
ids = []

for idx in range(len(YT_comments)):
    metadata.append({"Comment": YT_comments['Comment'][idx]})
    ids.append(str(YT_comments['index'][idx]))

# the good stuff
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="YT_comments_new")
collection.add(documents=documents, ids=ids)

# check the created collection
collection.peek()
collection.count()

# let's query this
results = collection.query(
    query_texts=["apple pay and the physical credit card", "2009 macbook pro"],
    n_results=3,
)
# voila mix multiple query types to arrive at the desired outcome
print("the outcome")
print(results)
