import chromadb
from langchain_chroma import Chroma
from unstructured.documents.elements import Element

# from langchain_huggingface import HuggingFaceEmbeddings

# embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
client = chromadb.HttpClient(
    host="localhost",
    port=6333,
)
client.reset()  # resets the database
collection = client.get_or_create_collection("my_collection")
# vector_db = Chroma(client=client, collection_name="my_collection",embedding_function=embedding_function,)


def add_to_db(data, ids):
    collection.upsert(documents=data, ids=ids)


def search(query, n_results=2):
    return collection.query(
        query_texts=[query],
        n_results=n_results,
    )["documents"]


if __name__ == "__main__":
    add_to_db("This is a document about pineapple", "1")
    add_to_db("This is a document about oranges", "2")
    print(search("This is a query document about hawaii")["documents"])
