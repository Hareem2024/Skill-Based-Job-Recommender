import axios from 'axios'
import { useAuthStore } from '@/store/authStore'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

export default api

// Auth endpoints
export const authAPI = {
  register: (data: { email: string; password: string; full_name?: string }) =>
    api.post('/auth/register', data),
  login: (email: string, password: string) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    return api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  getMe: (token?: string) => {
    const config = token ? { headers: { Authorization: `Bearer ${token}` } } : {}
    return api.get('/auth/me', config)
  },
}

// Resume endpoints
export const resumeAPI = {
  upload: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/resumes/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  getAll: () => api.get('/resumes/'),
  getOne: (id: number) => api.get(`/resumes/${id}`),
}

// Job endpoints
export const jobAPI = {
  getAll: (params?: { skip?: number; limit?: number; source?: string; title?: string }) =>
    api.get('/jobs/', { params }),
  getOne: (id: number) => api.get(`/jobs/${id}`),
  scrape: () => api.post('/jobs/scrape'),
  getMatches: (resumeId: number, minScore?: number) =>
    api.get(`/jobs/matches/${resumeId}`, { params: { min_score: minScore } }),
  matchResume: (resumeId: number) => api.post(`/jobs/match/${resumeId}`),
}

// Analytics endpoints
export const analyticsAPI = {
  getSkillAnalytics: (days?: number, topN?: number) =>
    api.get('/analytics/skills', { params: { days, top_n: topN } }),
  getSkillTrend: (skillName: string, days?: number) =>
    api.get(`/analytics/skills/${skillName}/trend`, { params: { days } }),
  getDemandForecast: (skillName?: string, daysAhead?: number) =>
    api.get('/analytics/demand-forecast', { params: { skill_name: skillName, days_ahead: daysAhead } }),
}

// Recommendation endpoints
export const recommendationAPI = {
  generateRoadmap: (resumeId: number) => api.post(`/recommendations/roadmap/${resumeId}`),
  generateProjects: (resumeId: number) => api.post(`/recommendations/projects/${resumeId}`),
  getAll: (type?: string) => api.get('/recommendations/', { params: { recommendation_type: type } }),
  getOne: (id: number) => api.get(`/recommendations/${id}`),
}

// Chat endpoints
export const chatAPI = {
  sendMessage: (message: string) => api.post('/chat/', { message }),
  getHistory: (limit?: number) => api.get('/chat/history', { params: { limit } }),
}

