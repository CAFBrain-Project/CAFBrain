import os
import streamlit as st
from io import BytesIO
from dotenv import load_dotenv

from agent.graph import graph
from agent.state import State

# from langchain.docstore.document import Document
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

    # img = st.session_state.graph.get_graph().draw_png()
    # st.image(img)

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

        st.session_state.chat_history.append(("Human", query))

        query = HumanMessage(content = query)
        if not state:
            state["messages"] = [query]
            state["source_file_paths"] = file_paths
            state["target_format"] = st.session_state.file_format
        else:
            state["messages"].append(query)
            state["source_file_paths"].extend(file_paths)
        
        conversation = [{"sender": sender,  "message": message} for sender, message in st.session_state.chat_history]
        # CSS for styling the messages
        st.markdown("""
            <style>
            .chat-container {
                max-width: 700px;
                margin: 0 auto;
                padding: 1rem;
            }
            .human {
                background-color: #DCF8C6;
                padding: 0.8rem;
                border-radius: 10px;
                margin-bottom: 0.5rem;
                align-self: flex-end;
                text-align: right;
            }
            .ai {
                background-color: #F1F0F0;
                padding: 0.8rem;
                border-radius: 10px;
                margin-bottom: 0.5rem;
                align-self: flex-start;
                text-align: left;
            }
            .message-block {
                display: flex;
                flex-direction: column;
                margin-bottom: 1rem;
            }
            </style>
        """, unsafe_allow_html = True)

        # Conversation container
        st.markdown('<div class="chat-container">', unsafe_allow_html = True)
        for msg in conversation:
            css_class = "human" if msg["sender"].lower() == "human" else "ai"
            st.markdown(f'<div class="message-block"><div class="{css_class}">{msg["message"]}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        with st.spinner("Thinking..."):
            st.session_state.graph_state = graph.invoke(state)

            # print(st.session_state.graph_state)
            st.session_state.chat_history.append(("AI", st.session_state.graph_state["messages"][-1].content))

with col2:
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
    
    ai_messages = st.session_state.graph_state.get("generated_content", [])
    if len(ai_messages):
        value = ai_messages[-1].content
    else:
        value = ""

    doc_content = st.text_area(label = "📝 Document Editor", value = value, height = 500, key = "editor")

    download_placeholder = st.empty()
    if st.button("🔧 Prepare Download"):
        processed_content = process_content(doc_content)

        buffer = BytesIO()
        
        file_format = st.session_state.file_format
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
