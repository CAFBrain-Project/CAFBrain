# CAFBrain

**Capital Area Food Bank's Generative AI Assistant** for Fundraising and Communications Teams

CAFBrain is an AI-powered Streamlit application designed to transform, query, and refine fundraising and communication materials. Built with LLMs, RAG (Retrieval-Augmented Generation), and multimodal input handling, it empowers users to generate grant proposals, blogs, presentations, and reports using their own source files—with full human-in-the-loop refinement and download support.

---

## 🚀 Features

- **LLM-Powered Generation**: Uses large language models (LLMs) to generate high-quality collateral.
- **RAG-Based Querying**: Ask questions and extract relevant insights from uploaded source documents.
- **Multimodal Input Support**: Accepts PDFs, PPTX, DOCX, TXT, and Images (with OCR for text extraction).
- **Human-in-the-Loop Refinement**: Users can iteratively refine outputs, upload additional supporting files, and regenerate content.
- **Template-Based Injection**: Outputs are fitted into user-provided templates (PPTX, PDF, DOCX).
- **Streamlit Web App Interface**: Fully interactive frontend to upload files, select modes, refine results, and download outputs.
- **Multiple Output Formats**: Download generated content as PowerPoint presentations, PDF reports, or HTML blogs.
- **Session Persistence**: Maintains session state for smooth transitions across multiple generations and refinements.

---

## 🛠️ Tech Stack

- Python 3.11+
- Streamlit
- LangChain
- Langgraph
- OpenAI API
- Unstructured (document parsing)
- PyMuPDF, pytesseract (image OCR)
- python-pptx (PowerPoint generation)
- FPDF (PDF generation)
- FastAPI (optional extension for backend APIs)

---

## ⚙️ How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/CAFBrain-Project/CAFBrain.git
cd CAFBrain
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set OpenAI API Key
```bash
export OPENAI_API_KEY=your-key-here
```

### 4. Launch the Streamlit App
```bash
streamlit run app.py
```

---

## 🧠 Workflow Overview

1. **Upload Source Files**
   - Supported types: PDF, PPTX, DOCX, TXT, Images.

2. **Choose Action Mode**
   - **Query**: Ask questions to retrieve specific information from your uploads.
   - **Generate New Content**: Create new grant proposals, blog posts, presentations, and reports.
   - **Refinement**: Refine existing generated content with extra supporting files.

3. **Optionally Upload Extra Files**
   - During refinement, users can add more documents to enhance outputs.

4. **Human-in-the-Loop Interaction**
   - Edit, regenerate, or query again for iterative improvement.

5. **Download Outputs**
   - Supported formats: PPTX (Presentations), PDF (Reports/Proposals), HTML (Blogs).

---

## ✨ Example Use Cases

| Scenario                                      | Action                         | Output                                    |
|-----------------------------------------------|--------------------------------|-------------------------------------------|
| Past grants + Strategic Plan                  | Generate New Grant Proposal    | Grant proposal emphasizing Food-as-Medicine leadership |
| Grant report + Interview Transcript           | Generate Blog Post             | Client-focused blog with embedded quotes |
| Strategic Plan + Budget Documents             | Generate Executive Presentation | Board-ready strategic deck                |
| New client interviews + prior blogs           | Refine Existing Content        | Updated blog with fresh testimonials      |

---

## 📌 Future Enhancements

- Drag-and-drop template selection
- Semantic search for deeper RAG-based querying
- In-app live editing of generated content
- Audit trail and versioning for refinements

---

## 🤝 Acknowledgements

This project is developed for the **Capital Area Food Bank** by us.  
Special thanks to the CAFB Fundraising, University of Maryland and Communications teams for continuous feedback, insights, and support.

---

## 📜 License

This project is currently licensed for internal use by Capital Area Food Bank.  