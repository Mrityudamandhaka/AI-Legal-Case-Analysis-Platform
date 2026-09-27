# LawMind – Legal Document Intelligence Engine

LawMind is an AI-powered legal document analysis platform that helps legal professionals and businesses analyze, understand, and assess legal documents with advanced risk scoring and summarization capabilities.

## 🚀 Key Features

- **Document Upload**: Upload PDF or TXT legal documents for analysis
- **Clause Extraction**: Automatically identify and classify legal clauses
- **Smart Summarization**: AI-generated summaries of complex legal documents
- **Risk Assessment**: Real-time risk scoring (0-100) with visual dashboard
- **Key Point Identification**: Extract important terms and conditions
- **Actionable Recommendations**: Get specific advice based on document content
- **Responsive UI**: Modern, user-friendly interface with real-time feedback

## 🧠 AI Capabilities

- **Cerebras API**: Legal clause extraction and classification
- **Meta Llama 3**: Document summarization and risk scoring
- **Dynamic Analysis**: Content-aware risk assessment based on document length and keywords
- **Real-time Processing**: Instant analysis and visualization of results

## 🛠️ Tech Stack

### Frontend
- **Next.js 15** - React framework for production-ready applications
- **TypeScript** - Strongly typed programming language
- **Tailwind CSS** - Utility-first CSS framework
- **Responsive Design** - Works on all device sizes

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.12** - Programming language
- **Uvicorn** - ASGI server implementation
- **Pydantic** - Data validation and settings management

### AI Services
- **Cerebras API** - Legal clause extraction
- **Meta Llama 3** - Document summarization and risk scoring

### Deployment
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container Docker applications

## 📁 Project Structure

```
lawmind/
├── backend/           # FastAPI backend service
│   ├── routes/        # API endpoints
│   ├── services/      # AI service integrations
│   └── main.py        # Application entry point
├── frontend/          # Next.js frontend application
│   ├── app/           # React components and pages
│   └── public/        # Static assets
├── docker/            # Docker configuration files
└── documents/         # Sample legal documents
```

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- Docker (optional, for containerized deployment)
- Cerebras API key
- Meta Llama 3 API key

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd lawmind
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   # Copy the example environment file and configure your API keys
   cp .env.example .env
   # Edit .env file with your actual API keys
   pip install -r requirements.txt
   python main.py
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the Application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Environment Variables

Create a `.env` file in the `backend` directory with the following variables:
- `CEREBRAS_API_KEY`: Your Cerebras API key for clause extraction
- `LLAMA_API_KEY`: Your Meta Llama 3 API key for summarization
- `SECRET_KEY`: Secret key for JWT token generation
- `DEBUG`: Set to True for development, False for production

**Note**: The `.env` file is ignored by Git to protect your API keys. Never commit actual API keys to the repository.

### Docker Deployment

```bash
# Build and start services
docker-compose up --build

# Stop services
docker-compose down
```

## 📊 Risk Assessment Features

LawMind provides comprehensive risk analysis for legal documents:

- **Dynamic Risk Scoring**: Risk scores (0-100) based on document content
- **Risk Level Classification**: Automatically categorized as Low, Medium-Low, Medium, High, or Very High
- **Content-Aware Analysis**: Different analysis for short, medium, and long documents
- **Keyword Detection**: Identifies specific legal terms (confidentiality, liability, termination, etc.)
- **Visual Dashboard**: Color-coded risk visualization with progress indicators
- **Key Points Extraction**: Important terms and conditions highlighted
- **Actionable Recommendations**: Specific advice based on document complexity

## 🎯 Use Cases

- **Contract Review**: Quickly analyze contracts for key terms and risks
- **Due Diligence**: Assess legal documents during business transactions
- **Compliance Checking**: Identify potential compliance issues
- **Legal Research**: Extract and classify clauses for further analysis
- **Risk Management**: Evaluate potential legal risks before signing agreements

## 🔧 API Endpoints

### Backend API (http://localhost:8000)

- `POST /upload/` - Upload and process legal documents
- `POST /extract/` - Extract and classify legal clauses
- `POST /summarize/` - Generate document summary with risk scoring
- `POST /analyze/` - Comprehensive document analysis

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Cerebras for providing the legal clause extraction API
- Meta for the Llama 3 language model
- The open-source community for the tools and libraries used in this project

## 📞 Support

For support, please open an issue on the GitHub repository or contact the development team.
