import time

from chatacter.settings import get_settings
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

settings = get_settings()
chat = ChatGroq(model_name="llama3-70b-8192", verbose=True)


def get_response(query, character):
    start_time = time.time()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Act as {character}. Answer in one statement."),
            ("human", "{text}"),
        ]
    )
    chain = prompt | chat
    try:
        response = chain.invoke({"text": query, "character": character})
    except Exception as e:
        end_time = time.time()
        return {"status": e, "time": end_time - start_time}
    end_time = time.time()
    return response.content, str(end_time - start_time)
