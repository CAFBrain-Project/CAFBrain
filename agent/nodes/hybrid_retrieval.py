from agent.state import State

from langchain_core.messages import HumanMessage
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def hybrid_retrieval(state: State):
    vectorstore = FAISS.load_local("agent/vectorstores/faiss", HuggingFaceEmbeddings(), allow_dangerous_deserialization = True)
    processed_doc_count = state.get("processed_doc_count", 0)
    documents = state.get("documents", [])
    similar_documents = state.get("similar_documents", [])
    
    last_message = state["messages"][-1].content

    # TODO: Do we need to get similar documents for every query?
    # Similar Documents related to query
    similar_documents.extend(vectorstore.similarity_search(last_message, k = 10))

    # Similar Documents related to User Documents
    # Vector Store Retrieval - Doc to Doc Retrieval
    # Query Documents - List[Document]
    # For each query_doc.page_content, find k similar documents in DB
    for file_documents in documents[processed_doc_count : ]:
        for document in file_documents:
            similar_documents.extend(vectorstore.similarity_search(document.page_content, k = 3))
        # TODO: Do we need score?
        # similar_documents.extend(vectorstore.similarity_search_with_score(document.page_content, k = 3))

    print("Hybrid Retrieval Complete")

    state["similar_documents"] = similar_documents

    return state