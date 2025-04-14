from agent.state import State
from agent.prompts import REFINE_TEMPLATE, CURRENT_ARTIFACT_TEMPLATE

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage

load_dotenv()
refine_model = ChatOpenAI(model = "gpt-4o-mini", temperature = 0, api_key = os.getenv("OPENAI_API_KEY")) # TODO: Move it to models dir

def refine(state: State):
    conversation = state["messages"]
    target_format = state["target_format"]
    artifacts = state["generated_content"]
    format_specifications = state["format_specifications"]
    extracted_content_details = state["extracted_content_details"]
    
    has_artifact = True if len(artifacts) > 0 else False
    artifact = artifacts[-1] if has_artifact else None
    
    artifact_content = CURRENT_ARTIFACT_TEMPLATE.replace("{artifact}", artifact.content)

    prompt = ChatPromptTemplate.from_template(REFINE_TEMPLATE)

    chain = prompt | refine_model | StrOutputParser()

    generated_content = chain.invoke({
        "conversation": conversation,
        "artifact_content": artifact_content,
        "extracted_content_details": extracted_content_details,
        "format_specifications": format_specifications,
        "target_format": target_format
    })

    state["generated_content"] = state.get("generated_content", []) + [AIMessage(content = generated_content)]

    print("Refine")

    return state