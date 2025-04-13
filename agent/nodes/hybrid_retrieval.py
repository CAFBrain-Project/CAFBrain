from agent.state import State

from langchain_core.messages import HumanMessage
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def hybrid_retrieval(state: State):
    vectorstore = FAISS.load_local("agent/vectorstores/faiss", HuggingFaceEmbeddings(), allow_dangerous_deserialization = True)
    similar_documents = state.get("similar_documents", [])
    
    last_message = ''
    for message in reversed(state["messages"]):
        if isinstance(message, HumanMessage):
            last_message = message.content
            break

    # Similar Documents related to query
    similar_documents.extend(vectorstore.similarity_search(last_message, k = 10))

    # Similar Documents related to User Documents
    # Vector Store Retrieval - Doc to Doc Retrieval
    # Query Documents - List[Document]
    # For each query_doc.page_content, find k similar documents in DB
    for document in state["documents"]:
        similar_documents.extend(vectorstore.similarity_search(document.page_content, k = 3))
        # similar_documents.extend(vectorstore.similarity_search_with_score(document.page_content, k = 3))

    print("Hybrid Retrieval Complete\n")
    return state | {"similar_documents": similar_documents}