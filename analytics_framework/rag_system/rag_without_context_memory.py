import os
import pandas as pd
import numpy as np
from analytics_framework.langchain.hello_world_lc import get_answer
from setup_chroma_vector_db import yt_data_read_process, chromadb_processing

if __name__ == '__main__':
    documents, ids = yt_data_read_process("../intake/data/YoutubeCommentsDataSet.csv",
                                          100,
                                          "Comment"
                                          )
    results = chromadb_processing(documents,
                                  ids,
                                  "YT_comments_new",
                                  "My macbook broke in an accident",
                                  )
    feed_the_llm = f'figure out how to fix this machine with the context from {results["documents"]}'
    answer = get_answer(feed_the_llm)
    print("AI Speaks:", answer)
