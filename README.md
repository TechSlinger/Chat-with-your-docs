# 📄 Chat with Your Doc: Intelligent Document Q&A System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent, full-stack document analysis application that allows users to upload PDF documents and ask complex questions about their content using advanced AI technologies.

## 🚀 Features

### Core Functionality
- **Multi-Document Upload**: Seamlessly upload and process multiple PDF files simultaneously
- **AI-Powered Q&A**: Get accurate, context-aware answers to complex questions about your documents
- **Real-time Processing**: Instant responses powered by advanced language models
- **Intuitive Interface**: Modern, responsive UI built with Streamlit

### Technical Capabilities
- **RAG Architecture**: Retrieval-Augmented Generation pipeline using LlamaIndex for grounded, accurate responses
- **Vector Embeddings**: Hugging Face sentence transformers for efficient document vectorization
- **Scalable Database**: Astra DB (Cassandra) integration for high-performance vector storage
- **Reduced Hallucinations**: Answers are strictly based on provided document content

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   LlamaIndex     │    │   Mistral AI    │
│   Frontend      │───▶│   RAG Pipeline   │───▶│   LLM           │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PDF Upload    │    │  Vector Store    │    │  Query Engine   │
│   Processing    │    │  (Astra DB)      │    │  Processing     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **Python**: Core programming language
- **LlamaIndex**: RAG framework and document processing
- **Astra DB**: Vector database (Cassandra-based)

### AI/ML
- **Mistral AI**: Large Language Model for question answering
- **Hugging Face Transformers**: Sentence embeddings generation
- **RAG (Retrieval-Augmented Generation)**: Architecture pattern
- **Natural Language Processing**: Document understanding

### Frontend
- **Streamlit**: Web application framework
- **Responsive Design**: Modern, user-friendly interface

## 📋 Prerequisites

- Python 3.8 or higher
- Astra DB account and credentials
- Mistral AI API key

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/chat-with-your-doc.git
   cd chat-with-your-doc
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database credentials
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
chat-with-your-doc/
│
├── app.py                 # Main Streamlit application
├── src/
│   ├── document_processor.py  # PDF processing and vectorization
│   ├── qa_engine.py           # Question-answering logic
│   └── database.py            # Astra DB integration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # Project documentation
└── assets/               # Images and static files
```

## 🔧 Configuration

Create a `.env` file with the following variables:

```env
MISTRAL_API_KEY=your_mistral_api_key
ASTRA_DB_TOKEN=your_astra_db_token
ASTRA_DB_ENDPOINT=your_astra_db_endpoint
HUGGINGFACE_API_TOKEN=your_huggingface_token
```

## 📖 Usage

1. **Upload Documents**: Use the file uploader to select one or multiple PDF files
2. **Wait for Processing**: The system will extract text and create vector embeddings
3. **Ask Questions**: Type your questions in natural language
4. **Get Answers**: Receive contextual, document-based responses instantly

## 🎯 Key Benefits

- **Accuracy**: RAG architecture ensures answers are grounded in your documents
- **Scalability**: Vector database handles large document collections efficiently  
- **User Experience**: Intuitive interface requires no technical expertise
- **Performance**: Fast similarity search and response generation
- **Flexibility**: Supports various document types and complex queries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LlamaIndex** for the powerful RAG framework
- **Mistral AI** for the language model capabilities
- **Streamlit** for the excellent web framework
- **DataStax Astra** for vector database infrastructure

## 📧 Contact

Your Name - [your.email@example.com](mailto:your.email@example.com)

Project Link: [https://github.com/your-username/chat-with-your-doc](https://github.com/your-username/chat-with-your-doc)

---

⭐ **If you found this project helpful, please give it a star!**