# Deployment Guide

This guide covers deploying the Intelligent Developer Hiring Portal to various platforms.

## Prerequisites

- Docker and Docker Compose installed
- Account on your chosen hosting platform
- OpenAI API key (for AI features)

## Deployment Options

### 1. Vercel (Frontend) + Render (Backend)

#### Frontend on Vercel

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   cd frontend
   vercel
   ```

3. **Set Environment Variables**:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL

#### Backend on Render

1. **Create a new Web Service** on Render
2. **Connect your repository**
3. **Configure**:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3.11

4. **Add Environment Variables**:
   - `DATABASE_URL`: PostgreSQL connection string
   - `REDIS_URL`: Redis connection string
   - `SECRET_KEY`: Generate a secure secret key
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `ALLOWED_ORIGINS`: Your frontend URL

5. **Add PostgreSQL Database**:
   - Create a PostgreSQL database on Render
   - Use the connection string as `DATABASE_URL`

6. **Add Redis Instance**:
   - Create a Redis instance on Render
   - Use the connection string as `REDIS_URL`

### 2. AWS (ECS/EKS)

#### Using Docker Compose on EC2

1. **Launch EC2 Instance**:
   - Use Ubuntu 22.04 LTS
   - Open ports: 80, 443, 8000, 3000

2. **Install Docker**:
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose -y
   ```

3. **Clone and Deploy**:
   ```bash
   git clone <your-repo>
   cd intelligent-dev-hiring-portal
   docker-compose up -d
   ```

4. **Set up Nginx** (reverse proxy):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:3000;
       }

       location /api {
           proxy_pass http://localhost:8000;
       }
   }
   ```

### 3. Docker Compose on VPS

1. **SSH into your VPS**
2. **Install Docker and Docker Compose**
3. **Clone repository**
4. **Start services**:
   ```bash
   docker-compose up -d
   ```

5. **Set up SSL with Let's Encrypt**:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://host:6379/0
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your-openai-api-key
DEBUG=False
LOG_LEVEL=INFO
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
```

## Database Migrations

After deployment, run migrations:

```bash
docker-compose exec backend alembic upgrade head
```

Or manually:

```bash
cd backend
alembic upgrade head
```

## Scaling

### Horizontal Scaling

- **Backend**: Run multiple FastAPI instances behind a load balancer
- **Celery Workers**: Scale workers based on job scraping load
- **Database**: Use read replicas for read-heavy operations

### Vertical Scaling

- Increase container resources (CPU, RAM)
- Optimize database queries
- Use caching (Redis) for frequently accessed data

## Monitoring

### Health Checks

- Backend: `GET /health`
- Frontend: Check if Next.js server responds

### Logging

- Backend logs: `docker-compose logs -f backend`
- Celery logs: `docker-compose logs -f celery_worker`
- Frontend logs: `docker-compose logs -f frontend`

## Security Checklist

- [ ] Use strong `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Set `DEBUG=False` in production
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Regular security updates
- [ ] Database backups
- [ ] Rate limiting on API endpoints

## Troubleshooting

### Database Connection Issues

- Check `DATABASE_URL` format
- Verify database is accessible
- Check firewall rules

### Redis Connection Issues

- Verify `REDIS_URL` is correct
- Check Redis is running
- Test connection: `redis-cli ping`

### Celery Not Processing Tasks

- Check Celery worker logs
- Verify Redis connection
- Ensure Celery Beat is running for scheduled tasks

## Backup Strategy

1. **Database Backups**:
   ```bash
   docker-compose exec postgres pg_dump -U postgres hiring_portal > backup.sql
   ```

2. **Restore**:
   ```bash
   docker-compose exec -T postgres psql -U postgres hiring_portal < backup.sql
   ```

## Performance Optimization

1. **Enable Caching**: Use Redis for frequently accessed data
2. **Database Indexing**: Add indexes on frequently queried columns
3. **CDN**: Use CDN for static assets
4. **Compression**: Enable gzip compression
5. **Image Optimization**: Optimize images in frontend

