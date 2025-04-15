from agent.state import State
from agent.prompts import QUERY_TEMPLATE

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage

load_dotenv()
query_model = ChatOpenAI(model = "gpt-4o-mini", temperature = 0, api_key = os.getenv("OPENAI_API_KEY")) # TODO: Move it to models dir

def query(state: State):
    conversation = state["messages"]
    retrieved_content = state["similar_documents"]
    
    prompt = ChatPromptTemplate.from_template(QUERY_TEMPLATE)

    chain = prompt | query_model | StrOutputParser()

    answer = chain.invoke({
        "conversation": conversation[:-1],
        "user_query": conversation[-1],
        "retrieved_content": retrieved_content
    })

    print("Query")
    print(answer)

    state["processed_doc_count"] = len(state["source_file_paths"])
    state["messages"].append(AIMessage(content = answer))

    return state