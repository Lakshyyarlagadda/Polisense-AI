# 🧬 PoliSense AI - Intelligent Employee Policy Assistant

A **Retrieval-Augmented Generation (RAG)** based chatbot that guides new employees through company onboarding using LLM technology. Built with LangChain, Streamlit, and Groq API.

## 📋 Overview

PoliSense AI is an intelligent, AI-powered chatbot designed to help new employees navigate company policies, procedures, and requirements efficiently. It uses:

- **RAG (Retrieval-Augmented Generation)**: Retrieves relevant company policy information from PDF documents
- **LLM (Large Language Model)**: Groq's Llama-3.1-8b-instant for intelligent, context-aware responses
- **Vector Store**: FAISS with HuggingFace embeddings for efficient document retrieval
- **Conversational Memory**: Maintains chat history for contextual conversations

## ✨ Features

- 🤖 **AI-Powered Assistance**: Conversational chatbot using state-of-the-art LLMs
- 📚 **Policy Retrieval**: Automatically retrieves relevant company policies from PDF documents
- 👤 **Personalized Responses**: Tailors answers based on employee information (department, position, etc.)
- 💬 **Conversation History**: Maintains message history for context-aware follow-ups
- ⚙️ **Adjustable Temperature**: Control LLM creativity via interactive slider
- 🎯 **Streaming Responses**: Real-time response streaming for better UX
- 🔐 **Security-Focused**: Built-in system prompts emphasize data security and compliance

## 🏗️ Project Structure

```
client-onboarding-rag-demo-solution/
├── app.py                 # Main Streamlit application
├── assistant.py           # Core AI assistant logic (RAG chain)
├── gui.py                 # Streamlit UI components
├── prompts.py             # System prompts and welcome messages
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── .gitignore            # Git ignore rules
├── .env                  # Environment variables (not committed)
├── data/
│   ├── employees.py      # Employee data generator
│   └── umbrella_corp_policies.pdf  # Company policies (PDF)
└── venv311/              # Python virtual environment
```

## 📦 Dependencies

- **langchain** (0.3.1+): Framework for building LLM applications
- **langchain-community** (0.3.1+): Community integrations
- **langchain-chroma** (0.1.4+): Chroma vector store integration
- **langchain-groq** (0.2.0+): Groq API integration
- **streamlit** (1.38.0+): Web UI framework
- **pypdf** (5.0.1+): PDF document loader
- **python-dotenv** (1.0.1+): Environment variable management
- **Faker** (30.0.0+): Employee data generation
- **sentence-transformers**: Embeddings model (installed via huggingface-embeddings)

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Groq API key (get one at [console.groq.com](https://console.groq.com))
- Company policy PDF file

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd client-onboarding-rag-demo-solution
   ```

2. **Create virtual environment**
   ```bash
   python3.11 -m venv venv311
   source venv311/bin/activate  # On Windows: venv311\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Add company policy PDF**
   Place your company policy PDF at `data/umbrella_corp_policies.pdf`

### Running the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 🔧 How It Works

### Architecture Flow

1. **Document Indexing** (First Run):
   - Load PDF from `data/umbrella_corp_policies.pdf`
   - Split into chunks (800 tokens, 150 token overlap)
   - Generate embeddings using HuggingFace's `all-MiniLM-L6-v2`
   - Store in FAISS vector database (cached)

2. **Employee Initialization**:
   - Generate random employee data with faker
   - Extract employee info (name, department, position, etc.)
   - Display in sidebar

3. **Conversation Flow**:
   - User asks a question
   - System retrieves top-3 relevant policy documents
   - LLM generates response using:
     - Employee context
     - Retrieved policies
     - Conversation history
     - System prompt guidelines
   - Response streamed to UI
   - Conversation saved to session state

### Key Components

#### `assistant.py`
Implements the `Assistant` class that manages:
- Conversation chain with RAG integration
- Message history handling
- Prompt template with employee context and retrieved policies
- LLM response generation with streaming

#### `gui.py`
Implements the `AssistantGUI` class that handles:
- Message rendering
- User input processing
- Employee information display
- Streamlit UI components

#### `app.py`
Main orchestrator that:
- Initializes Streamlit session state
- Loads and caches vector store
- Creates LLM and Assistant instances
- Renders the GUI
- Manages application state across reruns

#### `prompts.py`
Contains:
- **SYSTEM_PROMPT**: Detailed instructions for the AI assistant emphasizing security, professionalism, and context-aware responses
- **WELCOME_MESSAGE**: Welcome message for new employees

#### `data/employees.py`
Generates synthetic employee data with:
- Employee ID, name, email, phone
- Position and department
- Skills, location, hire date
- Supervisor and salary information

## ⚙️ Configuration

### Temperature Control
Adjust the "LLM Creativity" slider in the sidebar (0.0-1.0):
- **0.0**: Deterministic, factual responses (default: 0.3)
- **1.0**: Creative, varied responses

### Vector Store Settings
In `app.py`:
- `chunk_size`: 800 tokens per document chunk
- `chunk_overlap`: 150 tokens overlap between chunks
- `k`: 3 retrieved documents per query

### Embedding Model
Currently using `sentence-transformers/all-MiniLM-L6-v2`:
- Lightweight (22M parameters)
- Fast inference
- Good semantic understanding

## 📝 System Prompt Highlights

The assistant maintains:
- **Reserved, formal tone**: Professional communication suitable for corporate environment
- **Need-to-know basis**: Only provides necessary information
- **Security consciousness**: Emphasizes confidentiality and compliance
- **Personalization**: Uses employee-specific context for tailored responses
- **Clearance awareness**: Subtle references to information access restrictions

## 🔐 Security Considerations

- Store `GROQ_API_KEY` in `.env` (never commit this file)
- All conversation data stored in session state (cleared on browser close)
- PDF documents should contain company-appropriate content
- System prompt enforces information security guidelines

## 🐛 Troubleshooting

### "PDF file not found"
- Ensure `data/umbrella_corp_policies.pdf` exists
- Check file path in `app.py`

### "GROQ_API_KEY not found"
- Verify `.env` file exists in project root
- Check API key is valid at [console.groq.com](https://console.groq.com)

### Slow embedding generation
- First run caches embeddings (subsequent runs are fast)
- Consider using GPU if available for faster processing

### Memory issues with large PDFs
- Reduce `chunk_size` in app.py
- Increase `chunk_overlap` for better context

## 🎯 Use Cases

- **Employee Onboarding**: Guide new employees through HR policies
- **Policy Q&A**: Answer questions about company procedures
- **Compliance Training**: Ensure employees understand regulations
- **Self-Service Support**: Reduce HR support ticket volume
- **Knowledge Base**: Searchable company policy repository

## 🚦 Future Enhancements

- [ ] Multi-document support (multiple PDFs)
- [ ] Advanced analytics (query logs, common questions)
- [ ] Admin interface for policy updates
- [ ] Department-specific prompts
- [ ] Integration with HR systems
- [ ] Persistent conversation storage
- [ ] Multi-language support
- [ ] Custom embedding models

## 📄 License

This project is provided as-is for demonstration purposes.

## 👥 Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- All dependencies are documented
- Sensitive data is never committed

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review system logs in terminal
3. Verify all dependencies are installed: `pip list`
4. Test Groq API key validity

---

**Note**: PoliSense AI is designed as a flexible solution for any organization. Customize the company name, policies, and branding to match your organization's specific needs.
