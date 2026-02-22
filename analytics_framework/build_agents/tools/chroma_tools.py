import chromadb
from analytics_framework.build_agents.tools.catalog_tools import load_dataset

_client = chromadb.Client()


def embed_dataset(entry_name: str, text_column: str) -> str:
    """
    Embed a dataset column into ChromaDB for semantic search.

    Loads the dataset from the intake catalog, converts the specified
    text column into documents and stores them in a ChromaDB collection
    named after the entry.

    Args:
        entry_name: Catalog entry name (e.g. 'youtube_comments').
        text_column: Column whose text values will be embedded.

    Returns:
        Confirmation string with collection name and document count.
    """
    df, err = load_dataset(entry_name, n_rows=1000)
    if err:
        return err

    if text_column not in df.columns:
        return f"❌ Column '{text_column}' not found. Available: {df.columns.tolist()}"

    df = df[[text_column]].dropna().reset_index(drop=True)
    documents = df[text_column].astype(str).tolist()
    ids = [str(i) for i in range(len(documents))]

    collection = _client.get_or_create_collection(name=entry_name)
    collection.add(documents=documents, ids=ids)

    return f"✅ Embedded {len(documents)} rows from '{entry_name}' into ChromaDB collection '{entry_name}'."


def semantic_query(entry_name: str, query: str, n_results: int = 5) -> str:
    """
    Run a semantic search over an embedded dataset collection.

    Queries the ChromaDB collection for the closest matching documents
    to the natural language query. The collection must be embedded first
    via embed_dataset().

    Args:
        entry_name: ChromaDB collection name (same as catalog entry name).
        query: Natural language query string.
        n_results: Number of results to return.

    Returns:
        Formatted string of the top matching documents.
    """
    try:
        collection = _client.get_collection(name=entry_name)
    except Exception:
        return f"❌ No collection '{entry_name}' found. Run embed_dataset() first."

    results = collection.query(query_texts=[query], n_results=n_results)
    docs = results.get("documents", [[]])[0]

    if not docs:
        return "🔍 No results found."

    lines = [f"🔍 Top {len(docs)} results for: '{query}'\n"]
    for i, doc in enumerate(docs, 1):
        lines.append(f"  [{i}] {doc}")
    return "\n".join(lines)
