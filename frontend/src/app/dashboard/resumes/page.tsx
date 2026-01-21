'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import DashboardLayout from '@/components/layout/DashboardLayout'
import { resumeAPI, recommendationAPI } from '@/services/api'
import toast from 'react-hot-toast'
import { Upload, FileText, Sparkles, ChevronDown, ChevronUp, Clock, BookOpen, Target } from 'lucide-react'

export default function ResumesPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [resumes, setResumes] = useState<any[]>([])
  const [isUploading, setIsUploading] = useState(false)
  const [expandedResume, setExpandedResume] = useState<number | null>(null)
  const [recommendations, setRecommendations] = useState<Record<number, any[]>>({})
  const [loadingRecs, setLoadingRecs] = useState<Record<number, boolean>>({})

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/')
      return
    }
    fetchResumes()
  }, [isAuthenticated, router])

  const fetchResumes = async () => {
    try {
      const response = await resumeAPI.getAll()
      setResumes(response.data)
    } catch (error) {
      console.error('Error fetching resumes:', error)
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    if (!file.name.match(/\.(pdf|docx|doc)$/i)) {
      toast.error('Please upload a PDF or DOCX file')
      return
    }

    setIsUploading(true)
    try {
      await resumeAPI.upload(file)
      toast.success('Resume uploaded successfully!')
      fetchResumes()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Upload failed')
    } finally {
      setIsUploading(false)
    }
  }

  const fetchRecommendations = async (resumeId: number, type: 'roadmap' | 'project') => {
    setLoadingRecs(prev => ({ ...prev, [resumeId]: true }))
    try {
      const response = await recommendationAPI.getAll(type)
      setRecommendations(prev => ({
        ...prev,
        [resumeId]: response.data.filter((r: any) => r.recommendation_type === type)
      }))
    } catch (error) {
      console.error('Error fetching recommendations:', error)
    } finally {
      setLoadingRecs(prev => ({ ...prev, [resumeId]: false }))
    }
  }

  const handleGenerateRoadmap = async (resumeId: number) => {
    try {
      setLoadingRecs(prev => ({ ...prev, [resumeId]: true }))
      const response = await recommendationAPI.generateRoadmap(resumeId)
      
      if (response.data && response.data.length > 0) {
        toast.success(`Generated ${response.data.length} roadmap recommendations!`)
        // Display the generated recommendations
        setRecommendations(prev => ({
          ...prev,
          [resumeId]: [...(prev[resumeId] || []), ...response.data]
        }))
        setExpandedResume(resumeId)
      } else {
        toast.error('No recommendations were generated. Please try again.')
      }
    } catch (error: any) {
      console.error('Error generating roadmap:', error)
      toast.error(error.response?.data?.detail || 'Failed to generate roadmap')
    } finally {
      setLoadingRecs(prev => ({ ...prev, [resumeId]: false }))
    }
  }

  const handleGenerateProjects = async (resumeId: number) => {
    try {
      setLoadingRecs(prev => ({ ...prev, [resumeId]: true }))
      const response = await recommendationAPI.generateProjects(resumeId)
      
      if (response.data && response.data.length > 0) {
        toast.success(`Generated ${response.data.length} project suggestions!`)
        // Display the generated recommendations
        setRecommendations(prev => ({
          ...prev,
          [resumeId]: [...(prev[resumeId] || []), ...response.data]
        }))
        setExpandedResume(resumeId)
      } else {
        toast.error('No project suggestions were generated. Please try again.')
      }
    } catch (error: any) {
      console.error('Error generating projects:', error)
      toast.error(error.response?.data?.detail || 'Failed to generate projects')
    } finally {
      setLoadingRecs(prev => ({ ...prev, [resumeId]: false }))
    }
  }

  if (!isAuthenticated) return null

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">Resumes</h1>
            <p className="text-gray-400 mt-2">Upload and manage your resumes</p>
          </div>
          <label className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-primary-500 to-accent-500 text-white rounded-lg hover:from-primary-600 hover:to-accent-600 cursor-pointer shadow-lg transition-all">
            <Upload className="w-5 h-5 mr-2" />
            {isUploading ? 'Uploading...' : 'Upload Resume'}
            <input
              type="file"
              accept=".pdf,.docx,.doc"
              onChange={handleFileUpload}
              className="hidden"
              disabled={isUploading}
            />
          </label>
        </div>

        {resumes.length === 0 ? (
          <div className="glass-card rounded-xl p-12 text-center">
            <FileText className="w-16 h-16 text-gray-500 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-white mb-2">No resumes yet</h3>
            <p className="text-gray-400 mb-4">Upload your first resume to get started</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6">
            {resumes.map((resume) => (
              <div key={resume.id} className="glass-card rounded-xl p-6 glass-hover">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-white">{resume.file_name}</h3>
                    <p className="text-sm text-gray-400 mt-1">
                      Uploaded {new Date(resume.created_at).toLocaleDateString()}
                    </p>
                    {resume.extracted_skills && resume.extracted_skills.length > 0 && (
                      <div className="mt-4">
                        <p className="text-sm font-medium text-gray-300 mb-2">Extracted Skills:</p>
                        <div className="flex flex-wrap gap-2">
                          {resume.extracted_skills.slice(0, 10).map((skill: string, idx: number) => (
                            <span
                              key={idx}
                              className="px-3 py-1 glass text-primary-300 text-xs rounded-full border border-primary-500/30"
                            >
                              {skill}
                            </span>
                          ))}
                          {resume.extracted_skills.length > 10 && (
                            <span className="px-3 py-1 text-xs text-gray-500">
                              +{resume.extracted_skills.length - 10} more
                            </span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                  <div className="flex space-x-2 ml-4">
                    <button
                      onClick={() => handleGenerateRoadmap(resume.id)}
                      disabled={loadingRecs[resume.id]}
                      className="px-4 py-2 bg-gradient-to-r from-purple-500 to-purple-600 text-white text-sm rounded-lg hover:from-purple-600 hover:to-purple-700 flex items-center disabled:opacity-50 shadow-lg transition-all"
                    >
                      <Sparkles className="w-4 h-4 mr-1" />
                      {loadingRecs[resume.id] ? 'Generating...' : 'Roadmap'}
                    </button>
                    <button
                      onClick={() => handleGenerateProjects(resume.id)}
                      disabled={loadingRecs[resume.id]}
                      className="px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-600 text-white text-sm rounded-lg hover:from-green-600 hover:to-emerald-700 flex items-center disabled:opacity-50 shadow-lg transition-all"
                    >
                      <Sparkles className="w-4 h-4 mr-1" />
                      {loadingRecs[resume.id] ? 'Generating...' : 'Projects'}
                    </button>
                    {(recommendations[resume.id]?.length > 0 || expandedResume === resume.id) && (
                      <button
                        onClick={() => {
                          if (expandedResume === resume.id) {
                            setExpandedResume(null)
                          } else {
                            setExpandedResume(resume.id)
                            // If no recommendations loaded, fetch all recommendations
                            if (!recommendations[resume.id] || recommendations[resume.id].length === 0) {
                              recommendationAPI.getAll().then((response) => {
                                const allRecs = response.data.filter((r: any) => 
                                  r.recommendation_type === 'roadmap' || r.recommendation_type === 'project'
                                )
                                setRecommendations(prev => ({
                                  ...prev,
                                  [resume.id]: allRecs
                                }))
                              }).catch(console.error)
                            }
                          }
                        }}
                        className="px-4 py-2 glass text-gray-300 text-sm rounded-lg hover:bg-white/10 flex items-center transition-all"
                      >
                        {expandedResume === resume.id ? (
                          <>
                            <ChevronUp className="w-4 h-4 mr-1" />
                            Hide
                          </>
                        ) : (
                          <>
                            <ChevronDown className="w-4 h-4 mr-1" />
                            Show {recommendations[resume.id]?.length > 0 ? `(${recommendations[resume.id].length})` : ''}
                          </>
                        )}
                      </button>
                    )}
                  </div>
                </div>
                {expandedResume === resume.id && recommendations[resume.id] && recommendations[resume.id].length > 0 && (
                  <div className="mt-4 pt-4 border-t border-white/10">
                    <h4 className="text-sm font-semibold text-white mb-3">Recommendations:</h4>
                    <div className="space-y-3">
                      {recommendations[resume.id].map((rec) => (
                        <div key={rec.id} className="glass rounded-lg p-4">
                          <div className="flex items-start space-x-2 mb-2">
                            <Target className="w-5 h-5 text-primary-400 mt-0.5" />
                            <div className="flex-1">
                              <div className="flex items-center space-x-2 mb-1">
                                <h5 className="font-medium text-white">{rec.title}</h5>
                                <span className={`text-xs px-2 py-0.5 rounded ${
                                  rec.recommendation_type === 'roadmap' 
                                    ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30' 
                                    : 'bg-green-500/20 text-green-300 border border-green-500/30'
                                }`}>
                                  {rec.recommendation_type}
                                </span>
                              </div>
                              <p className="text-sm text-gray-300 mb-2">{rec.description}</p>
                              {rec.estimated_time && (
                                <div className="flex items-center text-xs text-gray-400 mb-1">
                                  <Clock className="w-3 h-3 mr-1" />
                                  {rec.estimated_time}
                                </div>
                              )}
                              {rec.resources && Array.isArray(rec.resources) && rec.resources.length > 0 && (
                                <div className="mt-2">
                                  <div className="flex items-center text-xs text-gray-400 mb-1">
                                    <BookOpen className="w-3 h-3 mr-1" />
                                    Resources:
                                  </div>
                                  <ul className="text-xs text-gray-300 ml-4 list-disc">
                                    {rec.resources.slice(0, 3).map((resource: string, idx: number) => (
                                      <li key={idx}>{resource}</li>
                                    ))}
                                    {rec.resources.length > 3 && (
                                      <li>+ {rec.resources.length - 3} more</li>
                                    )}
                                  </ul>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {expandedResume === resume.id && (!recommendations[resume.id] || recommendations[resume.id].length === 0) && !loadingRecs[resume.id] && (
                  <div className="mt-4 pt-4 border-t border-white/10 text-center text-gray-400 text-sm">
                    No recommendations yet. Click "Roadmap" or "Projects" to generate some!
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}

