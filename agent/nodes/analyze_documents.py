from agent.state import State
from agent.prompts import CAFB_TEMPLATE, EXTRACTION_CATEGORY_TEMPLATE, DEFAULT_EXTRACTION_TEMPLATE

import os
import re
from joblib import Memory
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
document_analyzer = ChatOpenAI(model = "gpt-4.1-mini", temperature = 0, api_key = os.getenv("OPENAI_API_KEY")) # TODO: Move it to models dir

cache_dir = "../cache"
memory = Memory(cache_dir, verbose=0)

@memory.cache
def cached_llm_call(text, extraction_types):
    extraction_categories_formatted = "\n".join([f"- {e}" for e in extraction_types])

    prompt_text = EXTRACTION_CATEGORY_TEMPLATE.format(
        extraction_categories=extraction_categories_formatted,
        text=text,
        category_1=extraction_types[0],
        category_2=extraction_types[1]
    )

    prompt = ChatPromptTemplate.from_template(prompt_text)

    chain = (
        prompt
        | document_analyzer
        | StrOutputParser()
    )

    response = chain.invoke({"text": text})
    return response

def analyze_documents(state: State):
    extracted_content_details = state.get('extracted_content_details', [])
    
    extraction_types = [
        "Key Points", "Quotes", "Statistics", "Themes",
        "Program Impacts", "Client Stories", "Funding Requirements",
        "Barriers Identified", "Food Medicine Leadership"
        # Add if needed
    ]

    processed_doc_count = state.get("processed_doc_count", 0)

    for index, text in enumerate(state["extracted_texts"]):
        if index < processed_doc_count:
            print(f'Skipping previously analyzed document: {index}')
            continue

        # Using cached call to avoid repetition
        response = cached_llm_call(text, tuple(extraction_types))

        print(f'Response for document {index}:\n{response}\n')

        # Parse response
        content_details = {}
        current_category = None

        for line in response.splitlines():
            line = line.strip()
            if line.startswith("# "):
                current_category = line[2:].strip()
                content_details[current_category] = []
            elif current_category and (line and (line[0].isdigit() or "No relevant information" in line)):
                content_details[current_category].append(line)

        extracted_content_details.append(content_details)

    print("Finished analyzing documents.\n")

    state["extracted_content_details"] = extracted_content_details

    return state