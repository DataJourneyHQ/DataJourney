import chromadb
import pandas as pd
import numpy as np

"""
# What's happening here?
# 1: read the dataset
# 2: convert to string (that's the format the db expects)
# 3: preferably set the index and then add to the db collection / or start simple
"""


def yt_data_read_process(file_path, num_rows, col_to_process):
    """
    :param file_path: string, path to the dataset
    :param num_rows: int, number of rows to read
    :param col_to_process: string, single column name
    :return: list, pre-processed data
    """
    yt_comments = pd.read_csv(file_path, dtype=str, nrows=num_rows)
    yt_comments.dropna(inplace=True)
    yt_comments.reset_index(inplace=True)

    metadata = []
    ids = []

    for idx in range(len(yt_comments)):
        metadata.append({"Comment": yt_comments['Comment'][idx]})
        ids.append(str(yt_comments['index'][idx]))

    return yt_comments[col_to_process].tolist(), ids


def chromadb_processing(documents, ids, db_collection_name, what_to_query, result_num=3):
    """
    :param documents: list,  pre-processed data
    :param ids: customised ids to generate embeddings
    :param db_collection_name: str, nice name for the collection
    :param what_to_query: str, drop your fav query text
    :param result_num: int, default set to 01
    :return: str, query outcome based on closest vector
    """

    # the good stuff
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection(name=db_collection_name)
    collection.add(documents=documents, ids=ids)

    # check the created collection
    collection.peek()
    collection.count()

    # let's query this
    outcome = collection.query(
        query_texts=[what_to_query],
        n_results=result_num,
    )
    return outcome


if __name__ == '__main__':
    documents, ids = yt_data_read_process("../intake/data/YoutubeCommentsDataSet.csv",
                                          1000,
                                          "Comment"
                                          )
    results = chromadb_processing(documents,
                                  ids,
                                  "YT_comments_new",
                                  "My macbook broke in an accident",
                                  )

    # voila mix multiple query types to arrive at the desired outcome
    print(f"The outcome for the query text \n {results}")
    # just the 'documents' part is interesting to us, let's scoop it out
    print(results["documents"])
