from agent.state import State
from agent.prompts import FOLLOWUP_TEMPLATE, NO_ARTIFACT_TEMPLATE, CURRENT_ARTIFACT_TEMPLATE

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage

load_dotenv()
follow_up_chat_model = ChatOpenAI(model = "gpt-4.1-nano", temperature = 0, api_key = os.getenv("OPENAI_API_KEY")) # TODO: Move it to models dir

def follow_up(state: State):
    artifacts = state.get("generated_content", [])
    has_artifact = True if len(artifacts) > 0 else False

    artifact = artifacts[-1] if has_artifact else None
    
    node = state["route"]
    current_artifact = CURRENT_ARTIFACT_TEMPLATE.replace("{artifact}", artifact.content) if has_artifact else NO_ARTIFACT_TEMPLATE
    conversation = state["messages"]

    prompt = ChatPromptTemplate.from_template(FOLLOWUP_TEMPLATE)

    chain = prompt | follow_up_chat_model | StrOutputParser()
    follow_up_text = chain.invoke({
        "node": node,
        "current_artifact": current_artifact,
        "conversation": conversation
    })

    print("Follow Up")
    print()

    state["processed_doc_count"] = len(state["source_file_paths"])
    state["messages"].append(AIMessage(content = follow_up_text))

    return state