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
    return yt_comments[col_to_process].tolist()


def chromadb_processing(documents, db_collection_name, what_to_query, result_num=1):
    """
    :param documents: list,  pre-processed data
    :param db_collection_name: str, nice name for the collection
    :param what_to_query: str, drop your fav query text
    :param result_num: int default set to 01
    :return: str, query outcome based on closest vector
    """
    metadata = []
    ids = []

    for idx in range(len(YT_comments)):
        metadata.append({"Comment": YT_comments['Comment'][idx]})
        ids.append(str(YT_comments['index'][idx]))

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
    documents = yt_data_read_process("../intake/data/YoutubeCommentsDataSet.csv",
                                     100,
                                     "Comment"
                                     )
    results = chromadb_processing(documents,
                                  "YT_comments_new",
                                  "My macbook broke",
                                  result_num=2
                                  )

    # voila mix multiple query types to arrive at the desired outcome
    print("the outcome")
    print(results)
