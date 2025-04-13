from langgraph.graph.message import add_messages
from langchain.docstore.document import Document
from typing_extensions import TypedDict, Annotated, List

class State(TypedDict):
    messages: Annotated[list, add_messages]

    prev_doc_count: int
    source_file_paths: List[str]
    
    extracted_texts: List[str]
    extracted_content_details: List[dict]

    documents: List[Document]
    similar_documents: List[Document]
    
    target_format: str
    format_specifications: str

    finished: str