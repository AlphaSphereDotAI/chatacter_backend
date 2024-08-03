import time
from typing import List

from chatacter.crawler import crawl
from chatacter.settings import load_settings
from chatacter.vector_database import add_data, get_chunks, query_db
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from qdrant_client.fastembed_common import QueryResponse

from App.chatacter.settings import Settings

settings: Settings = load_settings()
chat = ChatGroq(
    model_name="llama3-70b-8192",
    verbose=True,
)


def get_response(query: str, character: str) -> tuple[str, str]:
    start_time: float = time.time()
    print("Query:", query, "Character:", character)
    print("start crawling")
    links = crawl(query=query)
    print("start getting chunks")
    chunks = []
    for link in links:
        chunks.extend(get_chunks(url=link))
    print("start adding data to db")
    add_data(chunks=chunks)
    print("start querying db")
    results: List[QueryResponse] = query_db(query=query)
    prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        messages=[
            (
                "system",
                "Act as {character}. Answer in one statement. Answer the question using the provided context. Context: {context}",
            ),
            ("human", "{text}"),
        ]
    )
    chain = LLMChain(
        prompt=prompt,
        llm=chat,
        verbose=True,
    )
    response = chain.invoke(
        {"text": query, "character": character, "context": results[0]["text"]}
    )
    end_time: float = time.time()
    return str(object=response.content), str(object=end_time - start_time)
