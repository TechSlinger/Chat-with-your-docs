import streamlit as st
from astrapy import DataAPIClient
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.cassandra import CassandraVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.mistralai import MistralAI
from llama_index.core import Settings
import logging
import os
import tempfile
import shutil
import dotenv
# Load environment variables from .env file if present
dotenv.load_dotenv()
# Get API keys and tokens from environment variables
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
ASTRA_DB_TOKEN = os.getenv("ASTRA_DB_TOKEN")
ASTRA_DB_ENDPOINT = os.getenv("ASTRA_DB_ENDPOINT")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")
# --- Page Configuration ---
st.set_page_config(
    page_title="Chat with your doc",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Styling ---
def load_css():
    """Inject custom CSS for a modern UI."""
    st.markdown("""
    <style>
        /* General App Styling */
        .main {
            background-color: #F0F2F6;
        }

        /* Title and Headers */
        h1, h2, h3 {
            color: #1E1E1E;
            font-family: 'sans serif';
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 2px solid #E0E0E0;
        }

        /* Buttons Styling */
        .stButton>button {
            border-radius: 20px;
            border: 1px solid #4B8BBE;
            background-color: #4B8BBE;
            color: white;
            padding: 10px 24px;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #3A6A94;
            border-color: #3A6A94;
            color: white;
        }
        .stButton>button:focus {
            box-shadow: 0 0 0 2px #FFFFFF, 0 0 0 4px #4B8BBE;
        }

        /* File Uploader */
        [data-testid="stFileUploader"] {
            border: 2px dashed #4B8BBE;
            background-color: #F8F9FA;
            border-radius: 10px;
            padding: 20px;
        }
        [data-testid="stFileUploader"] label {
            color: #1E1E1E;
            font-size: 1.1em;
        }

        /* Text Input */
        [data-testid="stTextInput"] > div > div > input {
            border-radius: 10px;
            border: 1px solid #E0E0E0;
            padding: 10px;
        }
        
        /* Expander for source info */
        .st-expander {
            border: 1px solid #E0E0E0 !important;
            border-radius: 10px !important;
        }

        /* Custom containers */
        .info-box {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .answer-box {
            background-color: #E9F5FF;
            padding: 20px;
            border-left: 5px solid #4B8BBE;
            border-radius: 10px;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# --- Astra DB and Model Initialization (Cached) ---
# Use os.getenv to handle secrets in a way that works for both local dev and deployment
TOKEN = ASTRA_DB_TOKEN or "your_astra_db_token_here"
API_ENDPOINT = ASTRA_DB_ENDPOINT or "https://your-astra-db-endpoint.com"
MISTRAL_API_KEY = MISTRAL_API_KEY or "your_mistral_api_key_here"

@st.cache_resource
def initialize_models():
    """Initialize LLM and embedding models securely."""
    try:
        os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY
        llm = MistralAI(api_key=MISTRAL_API_KEY)
        embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-mpnet-base-v2")
        Settings.llm = llm
        Settings.embed_model = embed_model
        return llm, embed_model
    except Exception as e:
        st.error(f"Error initializing models: {e}", icon="🔥")
        return None, None

@st.cache_resource
def initialize_astra_db():
    """Initialize Astra DB connection securely."""
    try:
        client = DataAPIClient(TOKEN)
        database = client.get_database(API_ENDPOINT)
        return database
    except Exception as e:
        st.error(f"Error connecting to Astra DB: {e}", icon="🔥")
        return None

def process_uploaded_files(uploaded_files):
    """Process uploaded files, create vector index, and return it."""
    if not uploaded_files:
        return None, 0
    
    temp_dir = tempfile.mkdtemp()
    try:
        for uploaded_file in uploaded_files:
            with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
        
        documents = SimpleDirectoryReader(temp_dir).load_data()
        
        if not documents:
            st.error("No documents could be loaded. Please check your PDF files.", icon="📄")
            return None, 0
            
        index = VectorStoreIndex.from_documents(documents)
        return index, len(documents)
        
    except Exception as e:
        st.error(f"Error processing documents: {e}", icon="⚙️")
        return None, 0
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

# --- Main Application Logic ---
def main():
    load_css()

    # --- Sidebar ---
    with st.sidebar:
        st.header("Chat with your doc")
        st.markdown("""
        Welcome to your intelligent document assistant. 
        Upload your PDFs, and I'll help you find the answers you need.
        """)

        st.markdown("---")
        st.header("📋 Instructions")
        st.markdown("""
        1. **Upload**: Drag and drop one or more PDF files.
        2. **Process**: Click the 'Process Documents' button.
        3. **Query**: Ask any question about the document content.
        """)

        st.markdown("---")
        if 'documents_loaded' in st.session_state and st.session_state.documents_loaded:
            st.success("✅ Documents Processed & Ready!", icon="👍")
        else:
            st.info("⏳ Waiting for documents to be processed.", icon="⏳")

    # --- Main Content ---
    st.title("🤖 Ask Questions to Your Documents")
    st.markdown("Powered by Mistral AI and Astra DB for intelligent, fast, and scalable document analysis.")

    # File Upload Section
    with st.container():
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.header("Step 1: Upload Your PDFs")
        uploaded_files = st.file_uploader(
            "Choose your documents",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            if st.button("Process Documents", type="primary", use_container_width=True):
                with st.spinner("🧠 Analyzing documents... This may take a moment."):
                    index, doc_count = process_uploaded_files(uploaded_files)
                    
                    if index:
                        st.session_state.index = index
                        st.session_state.documents_loaded = True
                        st.success(f"Successfully processed {doc_count} document(s)!", icon="🎉")
                    else:
                        st.session_state.documents_loaded = False
                        st.error("Failed to process documents. Please try again.", icon="❌")
        st.markdown('</div>', unsafe_allow_html=True)


    # QA Section
    if st.session_state.get('documents_loaded', False):
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.header("Step 2: Ask Your Questions")
        
        user_question = st.text_input(
            "What would you like to know from your documents?",
            placeholder="e.g., What were the key findings in the financial report?",
            label_visibility="collapsed"
        )

        if user_question:
            with st.spinner("🔍 Searching for the best answer..."):
                try:
                    query_engine = st.session_state.index.as_query_engine()
                    response = query_engine.query(user_question)
                    
                    st.markdown('<div class="answer-box">', unsafe_allow_html=True)
                    st.subheader("📝 Here's the Answer:")
                    st.write(response.response)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    if hasattr(response, 'source_nodes') and response.source_nodes:
                        with st.expander("📚 View Source Information"):
                            for i, node in enumerate(response.source_nodes):
                                st.markdown(f"**Source {i+1} (Confidence: {node.score:.2f})**")
                                st.info(node.text[:500] + "...")
                                st.markdown("---")
                
                except Exception as e:
                    st.error(f"Error generating answer: {e}", icon="🔥")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👆 Upload and process your documents to activate the Q&A.", icon="⬆️")


if __name__ == "__main__":
    # Initialize models and DB connection
    llm, embed_model = initialize_models()
    if llm and embed_model:
        database = initialize_astra_db()
        main()

