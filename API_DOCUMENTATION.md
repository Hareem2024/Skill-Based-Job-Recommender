# API Documentation

Complete API documentation for the Intelligent Developer Hiring Portal.

Base URL: `http://localhost:8000/api/v1`

## Authentication

All endpoints except `/auth/register` and `/auth/login` require authentication via JWT token.

Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <token>
```

---

### Resumes

#### Upload Resume
```http
POST /resumes/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <resume.pdf>
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "file_name": "resume.pdf",
  "file_path": "uploads/1_resume.pdf",
  "extracted_text": "...",
  "extracted_skills": ["Python", "React", "Docker"],
  "created_at": "2024-01-01T00:00:00"
}
```

#### Get All Resumes
```http
GET /resumes/
Authorization: Bearer <token>
```

#### Get Resume by ID
```http
GET /resumes/{resume_id}
Authorization: Bearer <token>
```

---

### Jobs

#### Get Job Postings
```http
GET /jobs/?skip=0&limit=100&source=linkedin&title=developer
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records (default: 100, max: 1000)
- `source`: Filter by source (linkedin, indeed, stackoverflow)
- `title`: Search by job title

**Response:**
```json
[
  {
    "id": 1,
    "title": "Senior Python Developer",
    "company": "Tech Corp",
    "location": "San Francisco, CA",
    "source": "linkedin",
    "source_url": "https://linkedin.com/jobs/...",
    "description": "...",
    "required_skills": ["Python", "Django", "PostgreSQL"],
    "preferred_skills": ["AWS", "Docker"],
    "posted_date": "2024-01-01T00:00:00"
  }
]
```

#### Get Job by ID
```http
GET /jobs/{job_id}
Authorization: Bearer <token>
```

#### Trigger Job Scraping
```http
POST /jobs/scrape
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Scraping started",
  "task_id": "abc123"
}
```

#### Get Job Matches for Resume
```http
GET /jobs/matches/{resume_id}?min_score=50
Authorization: Bearer <token>
```

#### Match Resume to Jobs
```http
POST /jobs/match/{resume_id}
Authorization: Bearer <token>
```

---

### Analytics

#### Get Skill Analytics
```http
GET /analytics/skills?days=30&top_n=20
Authorization: Bearer <token>
```

**Response:**
```json
{
  "top_skills": [
    {"skill": "Python", "demand_count": 150},
    {"skill": "React", "demand_count": 120}
  ],
  "trends": {
    "daily_trends": {...},
    "growth_rates": {...}
  },
  "period_days": 30
}
```

#### Get Skill Trend
```http
GET /analytics/skills/{skill_name}/trend?days=90
Authorization: Bearer <token>
```

#### Get Demand Forecast
```http
GET /analytics/demand-forecast?skill_name=Python&days_ahead=30
Authorization: Bearer <token>
```

---

### Recommendations

#### Generate Learning Roadmap
```http
POST /recommendations/roadmap/{resume_id}
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Learn Docker",
    "description": "Master containerization...",
    "priority": 8,
    "estimated_time": "2 weeks",
    "resources": ["Docker docs", "Tutorial"],
    "reasoning": "High demand skill..."
  }
]
```

#### Generate Project Suggestions
```http
POST /recommendations/projects/{resume_id}
Authorization: Bearer <token>
```

#### Get All Recommendations
```http
GET /recommendations/?recommendation_type=roadmap
Authorization: Bearer <token>
```

#### Get Recommendation by ID
```http
GET /recommendations/{recommendation_id}
Authorization: Bearer <token>
```

---

### Chat

#### Send Message
```http
POST /chat/
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "What project should I build next?"
}
```

**Response:**
```json
{
  "response": "Based on your skills...",
  "message_id": 1
}
```

#### Get Chat History
```http
GET /chat/history?limit=50
Authorization: Bearer <token>
```

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message"
}
```

**Status Codes:**
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider:
- 100 requests per minute per user
- 1000 requests per hour per user

---

## WebSocket Support (Future)

WebSocket endpoints for real-time updates:
- `/ws/job-scraping/{task_id}` - Job scraping progress
- `/ws/recommendations/{user_id}` - New recommendations

---

## Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

Visit `http://localhost:8000/redoc` for ReDoc documentation.

