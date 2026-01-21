# Intelligent Developer Hiring Portal

A full-stack, ML-powered platform that analyzes job market trends, matches developer skills with job requirements, and generates personalized learning roadmaps and project suggestions.

## 🎯 Features

- **Live Job Scraping**: Automated scraping from LinkedIn and Glassdoor, filtered by resume skills and posted within 24 hours
- **Resume Analysis**: AI-powered resume parsing and skill extraction
- **Skill Matching**: Intelligent skill gap analysis with match scores
- **Personalized Recommendations**: AI-generated learning roadmaps and project suggestions
- **Interactive Dashboards**: Visual analytics with radar charts, heatmaps, and trend analysis
- **AI Chatbot**: Interactive mentor for project and learning guidance
- **Market Analytics**: Time-series forecasting for skill demand trends

## 🏗️ Architecture

```
┌─────────────┐
│   Frontend  │  React/Next.js
│  (Port 3000)│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   FastAPI   │  REST API + WebSocket
│  (Port 8000)│
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌──────┐ ┌────────┐
│PostgreSQL│ │  Redis  │
│         │ │ (Cache) │
└──────┘ └────┬───┘
              │
              ▼
         ┌─────────┐
         │ Celery  │  Background Workers
         │ Workers │  (Job Scraping)
         └─────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd intelligent-dev-hiring-portal

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Frontend runs on port 3000 by default (configurable in package.json)
```

#### Celery Worker

```bash
cd backend
celery -A app.celery_app worker --loglevel=info
```

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/              # API routes
│   │   ├── core/             # Configuration, security
│   │   ├── db/               # Database models & migrations
│   │   ├── ml/               # ML/AI modules
│   │   ├── services/         # Business logic
│   │   ├── tasks/            # Celery tasks
│   │   └── main.py           # FastAPI app
│   ├── tests/                # Unit tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Next.js pages
│   │   ├── services/         # API clients
│   │   └── utils/            # Utilities
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .github/workflows/        # CI/CD pipelines
└── README.md
```

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/hiring_portal
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your-openai-api-key
```

**Frontend (.env.local)**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📊 API Documentation

Full API documentation is available at `/docs` when the backend is running.

### Key Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/resumes/upload` - Upload resume
- `GET /api/jobs` - Get job listings
- `POST /api/jobs/scrape` - Trigger job scraping
- `GET /api/analytics/skills` - Get skill analytics
- `POST /api/recommendations/roadmap` - Generate learning roadmap
- `POST /api/chat` - AI chatbot endpoint

## 🤖 ML/AI Features

### Skill Extraction
- Uses transformer models for NLP-based skill extraction
- Normalizes skills across different naming conventions
- Extracts skills from both resumes and job postings

### Recommendation Engine
- Vector embeddings for similarity matching
- LLM-powered personalized recommendations
- Explains why each skill/project is suggested

### Market Analytics
- Time-series analysis of skill demand
- Trend forecasting using historical data
- Heatmaps for skill demand visualization

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🚢 Deployment

### Vercel (Frontend)
```bash
cd frontend
vercel deploy
```

### Render/AWS (Backend)
```bash
# Use provided Dockerfile
docker build -t hiring-portal-backend ./backend
docker run -p 8000:8000 hiring-portal-backend
```

## 📝 License

MIT License

## 👥 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

