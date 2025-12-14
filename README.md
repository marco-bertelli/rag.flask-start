# RAG Flask Starter

A Retrieval-Augmented Generation (RAG) chatbot API built with Flask, LlamaIndex, Pinecone, and MongoDB. This project provides a production-ready foundation for building AI-powered conversational applications with document retrieval capabilities.

## 🚀 Features

- **RAG-powered Chat**: Contextual responses using document retrieval with LlamaIndex
- **Multiple Source Types**: Support for PDF, CSV, and Q&A pairs as knowledge sources
- **Vector Search**: Pinecone integration for efficient similarity search
- **Persistent Storage**: MongoDB for chat history, user management, and index storage
- **Streaming Responses**: Real-time token streaming for chat responses
- **Rate Limiting**: Built-in rate limiting with Flask-Limiter
- **Authentication**: JWT-based authentication with admin and user roles
- **reCAPTCHA Support**: Google reCAPTCHA validation middleware
- **CORS Enabled**: Cross-Origin Resource Sharing support
- **Production Ready**: Gunicorn (Linux) and Waitress (Windows) server support

## 📋 Prerequisites

- Python 3.11+
- MongoDB instance
- Pinecone account and API key
- Perplexity API key (for LLM)
- (Optional) Google reCAPTCHA keys

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/marco-bertelli/rag.flask-start.git
   cd rag.flask-start
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # MongoDB
   MONGODB_URI=mongodb+srv://your-connection-string
   MONGODB_DATABASE=your-database-name
   
   # Security
   SECRET_KEY=your-jwt-secret-key
   
   # Pinecone
   PINECONE_API_KEY=your-pinecone-api-key
   PINECONE_ENV=your-pinecone-environment
   
   # Perplexity (LLM)
   PERPLEXITY_API_KEY=your-perplexity-api-key
   
   # OpenAI (optional)
   OPENAI_API_KEY=your-openai-api-key
   
   # reCAPTCHA (optional)
   RECAPTCHA_SECRET_KEY=your-recaptcha-secret-key
   ```

## 🚀 Running the Application

### Development (Windows)
```bash
python windows_waitress_start.py
```

### Production (Linux/Heroku)
```bash
gunicorn --preload --max-requests 500 --max-requests-jitter 5 -t 3 --worker-class gthread --timeout 120 index:app
```

The server will start on port `8080`.

## 📚 API Endpoints

### Chat Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/chats/me` | Get current user's chat | User Token |
| `GET` | `/chats/me/history` | Get chat history | User Token |
| `GET` | `/chats/guest` | Create a guest chat session | None |
| `GET` | `/chats/<chatId>/answer?answer=<query>` | Query the chatbot (streaming) | None |
| `PUT` | `/chats/message/<messageId>/feedback` | Set message feedback (good/bad) | None |

### Source Management Endpoints (Admin Only)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/index/source/<sourceType>` | Add a new source to the index | Admin Token |
| `DELETE` | `/index/source/<sourceId>` | Remove a source from the index | Admin Token |

### Source Types

- **qa**: Question-Answer pairs
  ```json
  { "question": "What is RAG?", "answer": "RAG stands for..." }
  ```
- **csv**: CSV file with questions and answers columns
  ```json
  { "path": "https://example.com/data.csv" }
  ```
- **pdf**: PDF document
  ```json
  { "path": "https://example.com/document.pdf" }
  ```

## 🏗️ Project Structure

```
rag.flask-start/
├── app.py                 # Flask app configuration
├── index.py               # Application entry point
├── index_manager.py       # LlamaIndex setup and management
├── conf.py                # Environment configuration loader
├── windows_waitress_start.py  # Windows server startup
├── Procfile               # Heroku/Gunicorn configuration
├── requirements.txt       # Python dependencies
├── data/                  # Sample data files
│   └── rules.pdf          # Initial document for indexing
├── apis/
│   ├── chats.py           # Chat API endpoints
│   └── sources.py         # Source management endpoints
├── middlewares/
│   ├── auth_middleware.py # JWT authentication
│   └── re_captcha.py      # reCAPTCHA validation
├── mongodb/
│   └── index.py           # MongoDB operations
└── utils/
    ├── chat_history_parser.py  # Chat history formatting
    ├── mongo_parsers.py        # MongoDB JSON encoder
    ├── parsers.py              # Document parsing utilities
    ├── validators.py           # Input validation
    └── vector_database.py      # Pinecone/MongoDB vector store setup
```

## ⚙️ Configuration

### LLM Settings

The project uses Perplexity's `mixtral-8x7b-instruct` model by default. Configuration is in `index_manager.py`:

```python
llm = Perplexity(
    api_key=os.getenv("PERPLEXITY_API_KEY"), 
    model="mixtral-8x7b-instruct", 
    temperature=0.2
)
```

### Embedding Model

Uses the local HuggingFace model `BAAI/bge-small-en-v1.5` for embeddings:

```python
Settings.embed_model = "local:BAAI/bge-small-en-v1.5"
```

### Rate Limits

Rate limits are configured in `apis/chats.py`:
- `/chats/me`: 5 requests per minute
- `/chats/me/history`: 15 requests per minute
- `/chats/<chatId>/answer`: 10 requests per minute

## 🔐 Authentication

The API uses JWT tokens for authentication. Include the token in the `Authorization` header:

```
Authorization: Bearer <your-jwt-token>
```

### User Roles
- **User**: Can access chat features
- **Admin**: Can manage knowledge sources (add/delete)
- **Guest**: Limited access with temporary chat sessions

## 📦 Dependencies

Key dependencies include:
- **Flask**: Web framework
- **LlamaIndex**: RAG framework
- **Pinecone**: Vector database
- **PyMongo**: MongoDB driver
- **Flask-Limiter**: Rate limiting
- **Flask-CORS**: CORS support
- **PyJWT**: JWT authentication
- **llmsherpa**: PDF parsing
- **Transformers & PyTorch**: ML models

## 🚢 Deployment

### Heroku

The project includes a `Procfile` for Heroku deployment:

```
web: gunicorn --preload --max-requests 500 --max-requests-jitter 5 -t 3 --worker-class gthread --timeout 120 index:app
```

### Docker (Custom)

Create a Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--preload", "-t", "120", "index:app"]
```

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Marco Bertelli**
- GitHub: [@marco-bertelli](https://github.com/marco-bertelli)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/marco-bertelli/rag.flask-start/issues).

---

⭐ Star this repository if you find it helpful!
