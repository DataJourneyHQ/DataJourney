import os
import pandas as pd
import numpy as np
from analytics_framework.langchain.hello_world_lc import get_answer
from setup_chroma_vector_db import yt_data_read_process, chromadb_processing

if __name__ == '__main__':
    get_answer()
