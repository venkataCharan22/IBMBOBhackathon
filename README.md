# Bug2PR - Autonomous Bug-to-PR Pipeline

An intelligent system that takes error logs, analyzes them through 8 specialized AI agents, and automatically creates GitHub pull requests with fixes, regression tests, and security audits.

## 🏗️ Architecture

```
Bug2PR/
├── backend/          # FastAPI + LangGraph + Python 3.11+
├── frontend/         # React 18 + Vite + Tailwind CSS
└── demo_app/         # Flask demo app with intentional bugs
```

## 🚀 Features

- **8 Specialized AI Agents**: Each agent handles a specific aspect of bug analysis and fixing
- **Multi-LLM Support**: Works with Ollama (local), Google Gemini, and Groq
- **Automated PR Creation**: Generates complete pull requests with:
  - Bug fix implementation
  - Regression tests
  - Security audit results
  - Detailed documentation
- **Vector Store Integration**: ChromaDB for semantic code search
- **Real-time Updates**: WebSocket support for live progress tracking

## 📋 Prerequisites

- Python 3.11+
- Node.js 20+
- Git
- Ollama (optional, for local LLM)

## 🛠️ Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:
- `GITHUB_TOKEN`: GitHub personal access token
- `GOOGLE_API_KEY`: Google Gemini API key (optional)
- `GROQ_API_KEY`: Groq API key (optional)
- `OLLAMA_BASE_URL`: Ollama server URL (default: http://localhost:11434)

### 3. Run Backend

```bash
# Development mode with auto-reload
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

## 🎨 Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Install Additional Packages

```bash
npm install tailwindcss axios @tanstack/react-query react-router-dom \
  framer-motion lucide-react react-syntax-highlighter react-dropzone
```

### 3. Configure Environment

```bash
cp .env.example .env
```

### 4. Run Frontend

```bash
npm run dev
```

Frontend will be available at: http://localhost:5173

## 📦 Project Structure

### Backend (`backend/`)

```
backend/
├── app/
│   ├── agents/          # AI agent implementations
│   ├── graph/           # LangGraph workflow definitions
│   ├── routes/          # FastAPI route handlers
│   ├── services/        # Business logic services
│   ├── utils/           # Utility functions
│   ├── config.py        # Configuration management
│   ├── database.py      # SQLite database setup
│   └── main.py          # FastAPI application entry point
├── requirements.txt     # Python dependencies
└── .env.example        # Environment variables template
```

### Frontend (`frontend/`)

```
frontend/
├── src/
│   ├── components/     # React components
│   ├── pages/          # Page components
│   ├── services/       # API service layer
│   ├── hooks/          # Custom React hooks
│   ├── styles/         # CSS and Tailwind styles
│   └── App.jsx         # Main application component
├── package.json        # Node dependencies
└── .env.example       # Environment variables template
```

## 🤖 AI Agents

The system uses 8 specialized agents:

1. **Error Analyzer**: Parses and categorizes error logs
2. **Code Locator**: Identifies the source of bugs in codebase
3. **Root Cause Analyzer**: Determines underlying issues
4. **Fix Generator**: Creates code fixes
5. **Test Generator**: Writes regression tests
6. **Security Auditor**: Checks for security vulnerabilities
7. **Documentation Writer**: Generates PR descriptions
8. **PR Creator**: Submits pull requests to GitHub

## 🔧 Configuration

### Backend Configuration

Key settings in `backend/.env`:

- **Application**: `APP_NAME`, `DEBUG`, `PORT`
- **Database**: `DATABASE_URL` (SQLite by default)
- **AI Models**: Configure Ollama, Google Gemini, or Groq
- **GitHub**: Repository access tokens
- **Agent Settings**: `MAX_ITERATIONS`, `AGENT_TIMEOUT`

### Frontend Configuration

Key settings in `frontend/.env`:

- **API Endpoint**: Backend server URL
- **Feature Flags**: Enable/disable features
- **Theme**: Customization options

## 🎯 Usage

1. **Upload Error Log**: Drag and drop or paste error logs
2. **Configure Analysis**: Select AI model and options
3. **Run Analysis**: Watch agents work in real-time
4. **Review Results**: See generated fix and tests
5. **Create PR**: Automatically submit to GitHub

## 🧪 Demo App

The `demo_app/` contains a Flask application with intentional bugs for testing:

```bash
cd demo_app
python app.py
```

## 📊 Database Schema

### Projects Table
- Stores project metadata and GitHub repository info

### Risks Table
- Tracks bugs, issues, and their resolution status

### Analysis Results Table
- Stores agent analysis outputs and confidence scores

## 🔐 Security

- API keys stored in environment variables
- GitHub tokens with minimal required permissions
- Security audit included in every PR
- Input validation and sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- LangChain & LangGraph for agent orchestration
- FastAPI for the backend framework
- React & Vite for the frontend
- Ollama for local LLM support

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/venkataCharan22/IBMBOBhackathon/issues)
- Documentation: See `/docs` folder

## 🗺️ Roadmap

- [ ] Support for more programming languages
- [ ] Integration with CI/CD pipelines
- [ ] Advanced code analysis features
- [ ] Team collaboration features
- [ ] Plugin system for custom agents

---

Built with ❤️ for the IBM BOB Hackathon