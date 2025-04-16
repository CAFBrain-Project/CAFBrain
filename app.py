import os
import json
import streamlit as st
from io import BytesIO
from dotenv import load_dotenv

from agent.graph import graph
from agent.state import State
from agent.utils import json_to_blog_html, json_to_presentation, json_to_pdf

from langchain_core.messages import HumanMessage

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

load_dotenv()
# openai_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY")
# hf_token = st.secrets["HF_TOKEN"] if "HF_TOKEN" in st.secrets else os.getenv("HF_TOKEN")

st.set_page_config(layout = "wide", page_title = "CAFBrain 🧠")

def process_content(document):
    return document    

# Toggle-able Sidebar
# with st.expander("⚙️ Settings", expanded = False):
#     # openai.api_key = st.text_input("🔑 OpenAI API Key", type="password")
#     model = st.selectbox("🧠 Model", ["gpt-3.5-turbo", "gpt-4"])
#     temperature = st.slider("🌡️ Temperature", 0.0, 1.0, 0.7)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pills_disabled" not in st.session_state:
    st.session_state.pills_disabled = False

if "user_input" not in st.session_state:
    st.session_state.user_input = None


if "file_format" not in st.session_state:
    st.session_state.file_format = None

if "graph" not in st.session_state:
    st.session_state.graph = graph

if "graph_state" not in st.session_state:
    st.session_state.graph_state = State()

# Main layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("💬 CAFBrain Assistant")

    user_input = st.chat_input(placeholder = "Your message", accept_file = "multiple", file_type = ["jpg", "png", "pdf", "txt", "pptx"])

    if not st.session_state.pills_disabled:
        file_format = st.pills("Choose file format", ["Text", "Grant Proposal", "Blog Post", "Presentation"])

        if file_format:
            st.session_state.file_format = file_format
    else:
        st.write("Selected format: " + st.session_state.file_format)


    if user_input != None:
        st.session_state.user_input = user_input

        if st.session_state.file_format:
            st.session_state.pills_disabled = True
            st.rerun()
        else:
            st.warning("Please select a file format before sending your message.")

    if (st.session_state.file_format != None
        and st.session_state.user_input != None):

        query = st.session_state.user_input.text
        files = st.session_state.user_input.files
        state = st.session_state.graph_state
        
        file_paths = []
        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.name)

            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            
            file_paths.append(file_path)

        st.session_state.chat_history.append(("Human", query))

        query = HumanMessage(content = query)
        if not state:
            state["messages"] = [query]
            state["source_file_paths"] = file_paths
            state["target_format"] = st.session_state.file_format
        else:
            state["messages"].append(query)
            state["source_file_paths"].extend(file_paths)

        with st.spinner("Thinking..."):
            st.session_state.graph_state = graph.invoke(state)
            st.session_state.chat_history.append(("AI", st.session_state.graph_state["messages"][-1].content))
        
        st.session_state.user_input = None

    conversation = [{"role": sender,  "message": message} for sender, message in st.session_state.chat_history]
    with st.container(height = 400, border = len(conversation)):
        for content in conversation:
            with st.chat_message(content["role"]):
                st.markdown(content["message"])

with col2:
    st.markdown("""
    <style>
        .stTextInput>div>textarea {
            font-size: 16px;
            padding: 12px;
            border-radius: 8px;
            border: 2px solid #4CAF50;
            width: 100%;
            box-sizing: border-box;
        }
                
        .stTextInput>div>textarea:focus {
            border-color: #45a049;
        }
                
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
        }
    </style>
    """, unsafe_allow_html = True)
    
    ai_messages = st.session_state.graph_state.get("generated_content", [])
    if len(ai_messages):
        value = ai_messages[-1].content
    else:
        value = ""

    doc_content = st.text_area(label = "📝 Document Editor", value = value, height = 500, key = "editor")

    download_placeholder = st.empty()
    mime = ""

    if st.button("🔧 Prepare Download"):
        processed_content = process_content(doc_content)

        buffer = BytesIO()
        
        file_format = st.session_state.file_format
        if file_format in ["Blog Post"]:
            processed_content = json_to_blog_html(doc_content)
            filename = f"blog_post.html"
            buffer.write(processed_content.encode("utf-8"))
            # Move to beginning of buffer
            buffer.seek(0)  
            # mime = "text/plain"
            mime = "text/html"


        elif file_format in ["Word Document"]:
            filename = f"content.docx"
            # doc = Document()
            # doc.add_paragraph(processed)
            # doc.save(buffer)
            mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        elif file_format in ["Grant Proposal"]:
            filename = f"content.pdf"
            buffer = json_to_pdf(doc_content)
            mime = "application/pdf"

        elif file_format in ["Presentation"]:
            filename = f"content.pptx"
            buffer = json_to_presentation(doc_content)
            mime = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

        print(mime)

        if mime == "":
            st.download_button(
            label = f"Nothing to download yet",
            data = ""
        )
        else:
            # Download button
            st.download_button(
                label = f"📥 Download {file_format.upper()} file",
                data = buffer,
                file_name = filename,
                mime = mime
            )
