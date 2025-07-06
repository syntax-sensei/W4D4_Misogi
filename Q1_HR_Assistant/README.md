# HR Knowledge Assistant

An intelligent HR policy assistant built with Streamlit and RAG (Retrieval-Augmented Generation) that helps employees find answers to HR-related questions using company policy documents.

## Features

- **Document Upload**: Upload HR policy documents (PDF, DOCX, TXT)
- **Intelligent Chunking**: HR-aware text chunking for better context
- **Vector Search**: Semantic search through policy documents
- **Conversational Interface**: Natural language Q&A about HR policies
- **Source Citations**: References to specific policy documents
- **Query Categorization**: Automatic categorization of questions (benefits, leave, conduct, etc.)

## Use Cases

- "How many vacation days do I get as a new employee?"
- "What's the process for requesting parental leave?"
- "Can I work remotely and what are the guidelines?"
- "How do I enroll in health insurance?"

## Project Structure

```
Q1_HR_Assistant/
├── app.py                       # Streamlit UI
├── rag_pipeline.py             # Query handling & response generation
├── embedder.py                 # Embedding + vector store
├── chunker.py                  # HR-aware chunking logic
├── extractor.py                # Multi-format text extractor
├── utils.py                    # Category classification etc.
├── requirements.txt
├── .env                        # OpenAI key
└── uploads/                    # Uploaded HR docs
```

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Q1_HR_Assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ADMIN_PASSWORD=your_secure_admin_password_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Usage

### Admin Mode
1. Switch to "Admin Upload" mode in the sidebar
2. Enter the admin password (set in your `.env` file) (Demo : Admin_hun_Mein@1321)
3. Upload HR policy documents (PDF, DOCX, TXT)
4. Click "Process & Embed" to add documents to the knowledge base
5. Existing files in the uploads folder can be processed using "Process Existing Files"
6. Use the logout button in the sidebar to end admin session

### Employee Chat Mode
1. Switch to "Employee Chat" mode in the sidebar
2. Ask questions about HR policies in natural language
3. Receive answers with citations to relevant policy documents

## Included Policy Documents

The system comes with 10 sample HR policy documents:
- Vacation and Leave Policy
- Parental Leave Policy
- Remote Work Policy
- Health Insurance Enrollment
- Sick Leave Policy
- Employee Conduct Policy
- Employee Benefits Policy

## Technical Details

- **Frontend**: Streamlit
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **LLM**: OpenAI GPT-3.5-turbo
- **Text Extraction**: pdfplumber (PDF), python-docx (DOCX)

## API Requirements

- OpenAI API key for GPT-3.5-turbo access
- Internet connection for embedding model download

## Security

- **Environment Variables**: Admin password is stored in `.env` file, not in code
- **Password Protection**: Admin functions require authentication
- **Session Management**: Secure session handling with automatic logout
- **File Upload**: Restricted to specific file types (PDF, DOCX, TXT)

### Security Best Practices

1. **Change Default Password**: Always set a strong `ADMIN_PASSWORD` in your `.env` file
2. **Secure Environment**: Keep your `.env` file secure and never commit it to version control
3. **Regular Updates**: Keep dependencies updated for security patches
4. **Access Control**: Limit admin access to authorized personnel only

aa