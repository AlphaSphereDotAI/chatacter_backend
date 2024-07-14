import time
from chatacter.settings import get_settings
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from chatacter.vector_database import get_chunks, add_data, query_db
from chatacter.crawler import crawl

settings = get_settings()
chat = ChatGroq(model_name="llama3-70b-8192", verbose=True)


def get_response(query, character):
    start_time = time.time()
    print("Query:", query, "Character:", character)
    print("start crawling")
    links = crawl(query)
    print("start getting chunks")
    chunks = []
    for link in links:
        chunks.extend(get_chunks(link))
    print("start adding data to db")
    add_data(chunks)
    print("start querying db")
    results = query_db(query)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Act as {character}. Answer in one statement. Answer the question using the provided context. Context: {context}"),
            ("human", "{text}"),
        ]
    )
    chain = LLMChain(prompt=prompt, llm=chat, verbose=True, )
    response = chain.invoke({"text": query, "character": character, "context": results[0]["text"]})
    end_time = time.time()
    return response.content, str(end_time - start_time)
