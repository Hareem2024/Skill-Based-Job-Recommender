'use client'

import { useEffect, useState } from 'react'
import { jobAPI } from '@/services/api'
import Link from 'next/link'
import { ExternalLink } from 'lucide-react'

export default function RecentJobs() {
  const [jobs, setJobs] = useState<any[]>([])

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await jobAPI.getAll({ limit: 5 })
        setJobs(response.data)
      } catch (error) {
        console.error('Error fetching jobs:', error)
      }
    }

    fetchJobs()
  }, [])

  return (
    <div className="glass-card rounded-xl p-6">
      <h2 className="text-xl font-semibold text-white mb-4">Recent Job Postings</h2>
      <div className="space-y-4">
        {jobs.length === 0 ? (
          <p className="text-gray-400">No jobs found. Trigger scraping to get started.</p>
        ) : (
          jobs.map((job) => (
            <div key={job.id} className="border-b border-white/10 pb-4 last:border-b-0">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-medium text-white">{job.title}</h3>
                  <p className="text-sm text-gray-300">{job.company}</p>
                  <p className="text-xs text-gray-400 mt-1">{job.location}</p>
                </div>
                {job.source_url && (
                  <a
                    href={job.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary-400 hover:text-primary-300 transition-colors"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

