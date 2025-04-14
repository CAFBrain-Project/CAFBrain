from typing_extensions import TypedDict, List
from langchain.docstore.document import Document
from langchain_core.messages.base import BaseMessage

class State(TypedDict):
    messages: List[BaseMessage]
    generated_content: List[BaseMessage]

    processed_doc_count: int
    source_file_paths: List[str]
    
    extracted_texts: List[str]
    extracted_content_details: List[dict]

    documents: List[List[Document]]
    similar_documents: List[Document]

    route: str
    
    target_format: str
    format_specifications: str