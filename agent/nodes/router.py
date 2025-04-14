from agent.state import State
from agent.prompts import ROUTE_QUERY_OPTIONS_HAS_ARTIFACTS, ROUTE_QUERY_OPTIONS_NO_ARTIFACTS, CURRENT_ARTIFACT_TEMPLATE, NO_ARTIFACT_TEMPLATE, ROUTE_QUERY_TEMPLATE

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
# gpt-4o
router_model = ChatOpenAI(model = "gpt-4o-mini", temperature = 0, api_key = os.getenv("OPENAI_API_KEY")) # TODO: Move it to models dir

def router(state: State):
    messages = state.get("messages", [])
    artifacts = state.get("generated_content", [])
    has_artifact = True if len(artifacts) > 0 else False

    query = messages[-1].content
    artifact = artifacts[-1].content if has_artifact else None
    
    artifact_options = ROUTE_QUERY_OPTIONS_HAS_ARTIFACTS if has_artifact else ROUTE_QUERY_OPTIONS_NO_ARTIFACTS
    current_artifact = CURRENT_ARTIFACT_TEMPLATE.replace("{artifact}", artifact) if has_artifact else NO_ARTIFACT_TEMPLATE

    prompt = ChatPromptTemplate.from_template(ROUTE_QUERY_TEMPLATE)

    chain = prompt | router_model | StrOutputParser()
    route = chain.invoke({"query": query, "artifact_options": artifact_options, "current_artifact": current_artifact})

    state["route"] = route

    print("Query:", messages[-1].content)
    print("Router:", route)

    return state