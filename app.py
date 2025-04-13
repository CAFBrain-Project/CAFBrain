import os
import streamlit as st
from io import BytesIO
from dotenv import load_dotenv

from agent.graph import graph
from agent.state import State

from langchain.docstore.document import Document
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
    st.header("💬 Assistant Chat")

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
        # "Take this pdf and this one PowerPoint presentation and write me a new blog post that emphasizes CAFB’s role as a leader in the food is medicine space. Ask me for the template of the new grant proposal and draft answers to all the questions using the source material without being repetitive between questions."
        files = st.session_state.user_input.files
        state = st.session_state.graph_state
        
        file_paths = []
        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.name)

            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            
            file_paths.append(file_path)
            
            # print(file.keys())
#         [UploadedFile(file_id='5a8bd2c9-9b5b-43af-8669-eb48d743d39a', name='001_01.12.23 CAFB & Feeding America Meeting.pptx', type='application/vnd.openxmlformats-officedocument.presentationml.presentation', size=10764969, _file_urls=file_id: "5a8bd2c9-9b5b-43af-8669-eb48d743d39a"
# upload_url: "/_stcore/upload_file/1dbeafec-408a-4098-8254-de4add452609/5a8bd2c9-9b5b-43af-8669-eb48d743d39a"
# delete_url: "/_stcore/upload_file/1dbeafec-408a-4098-8254-de4add452609/5a8bd2c9-9b5b-43af-8669-eb48d743d39a"
# ), UploadedFile(file_id='4c1aa65f-fa90-437f-8114-335cafcf0a30', name='002_2024 CAFB Strategy Refresh_external.pptx', type='application/vnd.openxmlformats-officedocument.presentationml.presentation', size=7297229, _file_urls=file_id: "4c1aa65f-fa90-437f-8114-335cafcf0a30"
# upload_url: "/_stcore/upload_file/1dbeafec-408a-4098-8254-de4add452609/4c1aa65f-fa90-437f-8114-335cafcf0a30"
# delete_url: "/_stcore/upload_file/1dbeafec-408a-4098-8254-de4add452609/4c1aa65f-fa90-437f-8114-335cafcf0a30"
# )]


        st.session_state.chat_history.append(("Human", query))
        if not state:
            state["messages"] = [query]
            state["prev_doc_count"] = 0
            state["source_file_paths"] = file_paths
            state["target_format"] = st.session_state.file_format
        else:
            state["messages"].append(query)
        
        print(state)

        with st.spinner("Thinking..."):
            st.session_state.graph_state = graph.invoke(state)
            st.session_state.chat_history.append(("AI", st.session_state.graph_state["messages"][-1].content))
        
        print(len(st.session_state.chat_history[-1][1]))

    # for role, msg in st.session_state.chat_history[-6:]:
    #     st.markdown(f"**{role}**: {msg}")

with col2:
    # print("\n".join([a + ": " + b for a, b in st.session_state.chat_history]))

    # st.header("")
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
    
    ai_messages = list(filter(lambda x: x[0] == "AI", st.session_state.chat_history))
    if len(ai_messages):
        value = ai_messages[-1][1]
    else:
        value = ""

    doc_content = st.text_area(label = "📝 Document Editor", value = value, height = 500, key = "editor")

    download_placeholder = st.empty()
    if st.button("🔧 Prepare Download"):
        processed_content = process_content(doc_content)

        buffer = BytesIO()
        
        file_format = st.session_state.file_format
        print("Processing")
        if file_format in ["Blog Post"]:
            filename = f"content.txt"
            buffer.write(processed_content.encode())
            mime = "text/plain"

        elif file_format in ["Word Document"]:
            filename = f"content.docx"
            # doc = Document()
            # doc.add_paragraph(processed)
            # doc.save(buffer)
            mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        elif file_format in ["Grant Proposal"]:
            filename = f"content.pdf"
            # pdf = FPDF()
            # pdf.add_page()
            # pdf.set_auto_page_break(auto=True, margin=15)
            # pdf.set_font("Arial", size=12)
            # for line in processed.split("\n"):
                # pdf.multi_cell(0, 10, line)
            # pdf.output(buffer)
            mime = "application/pdf"

        elif file_format in ["Presentation"]:
            filename = f"content.pptx"
            # ppt = Presentation()
            # slide_layout = ppt.slide_layouts[1]
            # slide = ppt.slides.add_slide(slide_layout)
            # title = slide.shapes.title
            # content_box = slide.placeholders[1]
            # title.text = "Processed Content"
            # content_box.text = processed
            # ppt.save(buffer)
            mime = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

        # Move to beginning of buffer
        buffer.seek(0)

        print(mime)

        # Download button
        st.download_button(
            label = f"📥 Download {file_format.upper()} file",
            data = buffer,
            file_name = filename,
            mime = mime
        )
