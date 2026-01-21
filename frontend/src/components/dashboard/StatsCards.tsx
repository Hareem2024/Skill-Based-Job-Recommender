'use client'

import { useEffect, useState } from 'react'
import { resumeAPI, jobAPI, recommendationAPI } from '@/services/api'
import { FileText, Briefcase, Target, TrendingUp } from 'lucide-react'

export default function StatsCards() {
  const [stats, setStats] = useState({
    resumes: 0,
    jobs: 0,
    recommendations: 0,
    matchScore: 0,
  })

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [resumesRes, jobsRes, recommendationsRes] = await Promise.all([
          resumeAPI.getAll(),
          jobAPI.getAll({ limit: 1 }),
          recommendationAPI.getAll(),
        ])
        
        setStats({
          resumes: resumesRes.data.length,
          jobs: jobsRes.data.length,
          recommendations: recommendationsRes.data.length,
          matchScore: 0, // Calculate from matches
        })
      } catch (error) {
        console.error('Error fetching stats:', error)
      }
    }

    fetchStats()
  }, [])

  const cards = [
    { icon: FileText, label: 'Resumes', value: stats.resumes, color: 'bg-blue-500' },
    { icon: Briefcase, label: 'Jobs', value: stats.jobs, color: 'bg-green-500' },
    { icon: Target, label: 'Recommendations', value: stats.recommendations, color: 'bg-purple-500' },
    { icon: TrendingUp, label: 'Avg Match Score', value: `${stats.matchScore}%`, color: 'bg-orange-500' },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card) => {
        const Icon = card.icon
        return (
          <div key={card.label} className="glass-card rounded-xl p-6 glass-hover">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-400">{card.label}</p>
                <p className="text-2xl font-bold text-white mt-2">{card.value}</p>
              </div>
              <div className={`${card.color} p-3 rounded-lg bg-opacity-20 backdrop-blur`}>
                <Icon className="w-6 h-6 text-white" />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

