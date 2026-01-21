'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import DashboardLayout from '@/components/layout/DashboardLayout'
import { jobAPI, resumeAPI } from '@/services/api'
import toast from 'react-hot-toast'
import { RefreshCw, Search, ExternalLink } from 'lucide-react'

export default function JobsPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [jobs, setJobs] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedSource, setSelectedSource] = useState('')

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/')
      return
    }
    fetchJobs()
  }, [isAuthenticated, router])

  const fetchJobs = async () => {
    setIsLoading(true)
    try {
      const response = await jobAPI.getAll({
        title: searchTerm || undefined,
        source: selectedSource || undefined,
        limit: 50,
      })
      setJobs(response.data)
    } catch (error) {
      console.error('Error fetching jobs:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleScrape = async () => {
    try {
      await jobAPI.scrape()
      toast.success('Job scraping started! This may take a few minutes.')
      setTimeout(fetchJobs, 5000) // Refresh after 5 seconds
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to start scraping')
    }
  }

  const handleMatchResume = async (resumeId: number) => {
    try {
      await jobAPI.matchResume(resumeId)
      toast.success('Matching completed! Check your matches.')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Matching failed')
    }
  }

  if (!isAuthenticated) return null

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">Job Postings</h1>
            <p className="text-gray-400 mt-2">Browse and match with job opportunities</p>
          </div>
          <button
            onClick={handleScrape}
            className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-primary-500 to-accent-500 text-white rounded-lg hover:from-primary-600 hover:to-accent-600 shadow-lg transition-all"
          >
            <RefreshCw className="w-5 h-5 mr-2" />
            Scrape Jobs
          </button>
        </div>

        <div className="glass-card rounded-xl p-4">
          <div className="flex space-x-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Search jobs..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && fetchJobs()}
                  className="w-full pl-10 pr-4 py-2 glass rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-white placeholder-gray-500 bg-transparent"
                />
              </div>
            </div>
            <select
              value={selectedSource}
              onChange={(e) => setSelectedSource(e.target.value)}
              className="px-4 py-2 glass rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-white bg-transparent"
            >
              <option value="" className="bg-black">All Sources</option>
              <option value="linkedin" className="bg-black">LinkedIn</option>
              <option value="glassdoor" className="bg-black">Glassdoor</option>
            </select>
            <button
              onClick={fetchJobs}
              className="px-4 py-2 glass text-white rounded-lg hover:bg-white/10 transition-all"
            >
              Filter
            </button>
          </div>
        </div>

        {isLoading ? (
          <div className="text-center py-12">
            <p className="text-gray-400">Loading jobs...</p>
          </div>
        ) : jobs.length === 0 ? (
          <div className="glass-card rounded-xl p-12 text-center">
            <p className="text-gray-400">No jobs found. Try scraping jobs to get started.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6">
            {jobs.map((job) => (
              <div key={job.id} className="glass-card rounded-xl p-6 glass-hover">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-white">{job.title}</h3>
                    <p className="text-lg text-gray-300 mt-1">{job.company}</p>
                    <p className="text-sm text-gray-400 mt-1">{job.location}</p>
                    {job.required_skills && job.required_skills.length > 0 && (
                      <div className="mt-4">
                        <p className="text-sm font-medium text-gray-300 mb-2">Required Skills:</p>
                        <div className="flex flex-wrap gap-2">
                          {job.required_skills.slice(0, 8).map((skill: string, idx: number) => (
                            <span
                              key={idx}
                              className="px-3 py-1 glass text-accent-300 text-xs rounded-full border border-accent-500/30"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                    {job.description && (
                      <p className="text-sm text-gray-400 mt-4 line-clamp-3">
                        {job.description.substring(0, 200)}...
                      </p>
                    )}
                  </div>
                  <div className="ml-4 flex flex-col space-y-2">
                    {job.source_url && (
                      <a
                        href={job.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-primary-500 to-accent-500 text-white text-sm rounded-lg hover:from-primary-600 hover:to-accent-600 shadow-lg transition-all"
                      >
                        <ExternalLink className="w-4 h-4 mr-1" />
                        View Job
                      </a>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}

