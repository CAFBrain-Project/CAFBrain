from agent.state import State
from agent.prompts import CAFB_TEMPLATE, EXTRACTION_CATEGORY_TEMPLATES, DEFAULT_EXTRACTION_TEMPLATE

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
document_analyzer = ChatOpenAI(model = "gpt-3.5-turbo", temperature = 0, api_key = os.getenv("OPENAI_API_KEY")) # TODO: Move it to models dir

def analyze_documents(state: State):
    extracted_content_details = state.get('extracted_content_details', [])
    extraction_types = ["Key Points", "Quotes", "Statistics", "Themes",                                                                  # Core
                    # "Program Impacts", "Client Stories", "Funding Requirements", "Barriers Identified", "Food Medicine Leadership"       # Optional
                ]

    processed_doc_count = state.get("processed_doc_count", 0)
    for text in state["extracted_texts"][processed_doc_count : ]:
        content_details = dict()

        for extraction_type in extraction_types:
            category_prompt = EXTRACTION_CATEGORY_TEMPLATES.get(extraction_type, DEFAULT_EXTRACTION_TEMPLATE.replace("{extraction_type}", extraction_type))
            prompt = ChatPromptTemplate.from_template(CAFB_TEMPLATE + category_prompt)
    
            chain = (
                prompt
                | document_analyzer
                | StrOutputParser()
            )
    
            content_details[extraction_type] = chain.invoke({"text": text})
    
        extracted_content_details.append(content_details)

    print("Analyzed Documents")

    state["extracted_content_details"] = extracted_content_details

    return state
