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

    prev_doc_count = state.get("prev_doc_count", 0)
    for index, text in enumerate(state["extracted_texts"]):
        if(index < prev_doc_count):
            print('Skipping analysing previous documents')
            continue
        
        content_details = dict()

        for extraction_type in extraction_types:
            category_prompt = EXTRACTION_CATEGORY_TEMPLATES.get(extraction_type, DEFAULT_EXTRACTION_TEMPLATE.replace("{extraction_type}", extraction_type))
            prompt = ChatPromptTemplate.from_template(CAFB_TEMPLATE + category_prompt)

            print('This is the prompt of doc_analyzer:', prompt)
    
            chain = (
                prompt
                | document_analyzer
                | StrOutputParser()
            )
    
            content_details[extraction_type] = chain.invoke({"text": text})
    
        extracted_content_details.extend(content_details)
        print()

    print("Analyzed Documents")

    # TODO: Don't we have to add pipe operator here?
    return {"extracted_content_details": extracted_content_details}
