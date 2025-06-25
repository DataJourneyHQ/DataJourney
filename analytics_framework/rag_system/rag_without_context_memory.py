import os
import pandas as pd
import numpy as np
from tabulate import tabulate
from analytics_framework.langchain.hello_world_lc import get_answer
from setup_chroma_vector_db import yt_data_read_process, chromadb_processing

os.environ["TOKENIZERS_PARALLELISM"] = "false"

if __name__ == '__main__':
    # examples to get started
    example_query = "My macbook broke in an accident -> "
    example_prompt = "figure out how to fix this machine with the context from -> "

    # user inputs to have a good dynamic between user and system
    query_user = input(f"Input the text you want to search, eg: {example_query}")
    llm_user = input(f"Input the prompt to feed the llm running in background, eg: {example_prompt}")

    documents, ids = yt_data_read_process("../intake/data/YoutubeCommentsDataSet.csv",
                                          1000,
                                          "Comment"
                                          )
    results = chromadb_processing(documents,
                                  ids,
                                  "YT_comments_new",
                                  query_user,
                                  )
    feed_the_llm = f'{llm_user}{results["documents"]}'
    answer = get_answer(feed_the_llm)
    # show and tell
    data = [
        ["Document Search Result", str(feed_the_llm)],
        ["User Query", str(query_user)],
        ["AI Answer", answer]
    ]

    print(tabulate(data, headers=["Field", "Value"], tablefmt="fancy_grid"))
