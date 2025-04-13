from agent.state import State
from agent.prompts import CONTENT_GENERATION_BASE_TEMPLATE, GRANT_PROPOSAL_TEMPLATE, BLOG_POST_TEMPLATE, PRESENTATION_TEMPLATE

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
contente_generator = ChatOpenAI(model = "gpt-4o-mini", temperature = 0, api_key = os.getenv("OPENAI_API_KEY")) # TODO: Move it to models dir

def construct_generation_prompt(target_format):
    template = CONTENT_GENERATION_BASE_TEMPLATE

    if target_format == "Grant Proposal":
        template += GRANT_PROPOSAL_TEMPLATE

    elif target_format == "Blog Post":
        template += BLOG_POST_TEMPLATE

    elif target_format == "Presentation":
        template += PRESENTATION_TEMPLATE

    template += "\nGenerate the content now:"

    return ChatPromptTemplate.from_template(template)

def generate_content(state: State):
    target_format = state["target_format"]
    format_specifications = state["format_specifications"] 
    extracted_content_details = state["extracted_content_details"]
    
    prompt = construct_generation_prompt(target_format)
    chain = (
        prompt
        | contente_generator
        | StrOutputParser()
    )

    generated_content = chain.invoke({
        "extracted_content_details": extracted_content_details,
        "format_specifications": format_specifications,
        "target_format": target_format
    })

    print("Content Generated")
    print(generated_content)
    print("Generation END")
    print(len(generated_content))

    # TODO: Don't we need to wrap around AIMessage?
    return state | {"messages": [generated_content]}