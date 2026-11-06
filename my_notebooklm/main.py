import os
import tempfile
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# NEW: The Google Gemini engines
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

def load_documents(uploaded_files):
    """Routes files to the correct loader based on their extension."""
    documents = []
    
    # Create a temporary directory to store files while processing
    with tempfile.TemporaryDirectory() as temp_dir:
        for uploaded_file in uploaded_files:
            # 1. Save the Streamlit file to the temporary directory
            temp_filepath = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_filepath, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # 2. Check the extension to pick the right loader
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            try:
                if file_extension == ".pdf":
                    loader = PyPDFLoader(temp_filepath)
                elif file_extension == ".txt":
                    loader = TextLoader(temp_filepath)
                elif file_extension in [".doc", ".docx"]:
                    loader = Docx2txtLoader(temp_filepath)
                elif file_extension == ".csv":
                    loader = CSVLoader(temp_filepath)
                else:
                    st.warning(f"Unsupported file type: {file_extension}")
                    continue
                
                # 3. Extract the text and tag it with the original filename
                docs = loader.load()
                for doc in docs:
                    doc.metadata["source"] = uploaded_file.name
                
                documents.extend(docs)
                
            except Exception as e:
                st.error(f"Error loading {uploaded_file.name}: {e}")
                
    return documents

def create_vectorstore(documents, api_key):
    """Splits documents and stores them in a Chroma vector database using Gemini."""
    # 1. Slice the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    
    # 2. Convert text to numbers using Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001", 
        google_api_key=api_key
    )
    
    # 3. Store in Chroma
    vectorstore = Chroma.from_documents(chunks, embeddings)
    
    return vectorstore

def generate_summary(documents, api_key):
    """Generates a quick overview of the uploaded documents."""
    # Join the text from the first few pages (up to ~15,000 chars for speed)
    combined_text = "\n\n".join([doc.page_content for doc in documents])
    preview_text = combined_text[:15000] 
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash", 
        google_api_key=api_key,
        temperature=0.3 # Low temperature for factual summarization
    )
    
    prompt = f"""
    You are an AI assistant. I just uploaded a document. 
    Based on the text below, provide a brief, 3-4 sentence overview 
    explaining what this document is about. Keep it conversational.
    
    Document preview:
    {preview_text}
    """
    
    response = llm.invoke(prompt)
    return response.content

st.set_page_config(page_title="My NotebookLM", layout="wide")

# --- CUSTOM CSS FOR NOTEBOOKLM STYLE ---
st.markdown("""
<style>
    /* 1. Keep top header transparent so sidebar toggle button stays visible */
    header[data-testid="stHeader"] {
        background-color: transparent;
    }
    
    /* Hide top menu and footer only */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 2. Adjust top padding to maximize screen space */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* 3. Style the User Chat Bubbles */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #f0f4f9;
        border: none;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* 4. Style the AI Chat Bubbles */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: transparent;
        border: none;
        padding: 1rem;
    }
    
    /* 5. Tweak typography for readability */
    .stMarkdown p {
        font-size: 16px;
        line-height: 1.6;
        color: #1f1f1f;
    }
    
    /* 6. Clean up the file uploader */
    [data-testid="stFileUploadDropzone"] {
        background-color: #f8f9fa;
        border: 1px dashed #dcdcdc;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("My Documents")
    
    # change it to env variable
    api_key = "AQ.Ab8RN6K3LB2hKsXfzCUdP39G52v63idNmc1VlOw7yG-Wh8AZHA"
    uploaded_files = st.file_uploader(
        "Upload files here", 
        type=["pdf", "txt", "docx", "csv"], 
        accept_multiple_files=True
    )
    
    if uploaded_files and api_key:
        if st.button("Process Documents", use_container_width=True):
            with st.spinner("Reading and indexing files..."):
                # 1. Load and Chunk
                raw_docs = load_documents(uploaded_files)
                vectorstore = create_vectorstore(raw_docs, api_key)
                st.session_state["vectorstore"] = vectorstore
                
                # 2. Generate the Summary
                st.session_state["doc_summary"] = generate_summary(raw_docs, api_key)
                
                st.success("Documents processed and saved to memory!")
    elif uploaded_files and not api_key:
        st.warning("API key is not working. Contact the support team.")

    # --- RESET BUTTON ---
    st.divider()
    if st.button("🗑️ Reset All & Clear Chat", type="secondary", use_container_width=True):
        st.session_state.messages = []
        if "vectorstore" in st.session_state:
            del st.session_state["vectorstore"]
        if "raw_docs" in st.session_state:
            del st.session_state["raw_docs"]
        if "doc_summary" in st.session_state:
            del st.session_state["doc_summary"]
        st.rerun()
    
# --- THE CHAT INTERFACE ---
st.title("📓 My NotebookLM")

# --- DOCUMENT OVERVIEW ---
if "doc_summary" in st.session_state:
    with st.expander("📄 Document Overview", expanded=True):
        st.markdown(st.session_state["doc_summary"])

# 1. Initialize chat history in Streamlit's session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display previous chat messages when the app reruns
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. The Chat Input box
if prompt := st.chat_input("Ask a question about your documents..."):
    
    # Immediately display the user's question
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Save the user's question to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 4. Generate the AI Response
    with st.chat_message("assistant"):
        # Check if the database and API key exist first
        if "vectorstore" not in st.session_state:
            st.warning("Please enter your API key and process a document first!")
        elif not api_key:
            st.warning("Please enter your Gemini API key in the sidebar.")
        else:
            with st.spinner("Thinking..."):
                # A. Retrieve the top 3 most relevant chunks from ChromaDB
                retriever = st.session_state["vectorstore"].as_retriever(search_kwargs={"k": 3})
                relevant_docs = retriever.invoke(prompt)
                
                # B. Format the chunks into a single text block with source names
                context_text = "\n\n".join([
                    f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}" 
                    for doc in relevant_docs
                ])
                
                # C. Build the prompt for Gemini
                prompt_template = f"""
                    You are a helpful assistant. 

                    Instructions:
                    1. First, check if the question can be answered using the provided Context below. If it can, answer using that context and cite your sources.
                    2. If the answer is NOT in the provided Context, answer using your general world knowledge. However, you MUST explicitly state at the very beginning of your response: 
                    "⚠️ [General Knowledge]: This information was not found in your uploaded documents, but based on general knowledge..."

                    Context:
                    {context_text}

                    Question:
                    {prompt}
                    """
                
                # D. Call Gemini Pro
                llm = ChatGoogleGenerativeAI(
                    model="gemini-3.5-flash", 
                    google_api_key=api_key,
                    temperature=0 # Keep it factual, no hallucinations
                )
                
                response = llm.invoke(prompt_template)
                
                # E. Display the answer
                st.markdown(response.content)
                
                # F. Add a "Citations" dropdown so you can see exactly where it got the info!
                with st.expander("View Source Documents"):
                    for i, doc in enumerate(relevant_docs):
                        st.markdown(f"**Source {i+1}: {doc.metadata.get('source', 'Unknown')}**")
                        st.info(doc.page_content)
                
                # G. Save the AI's response to history
                st.session_state.messages.append({"role": "assistant", "content": response.content})