import chromadb
chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(name="datajourney")

collection.upsert(
    documents=["../intake/data/global_bleaching_environmental.csv"], #TODO: doesn't work, read and loop insertion
    ids=["dj_01"]
)

results = collection.query(
    query_texts=["This is a query document about North Norman's Pond Cay Patch"],
    n_results=2
)

print(results)
