'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import DashboardLayout from '@/components/layout/DashboardLayout'
import { analyticsAPI } from '@/services/api'
import { Line, Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)

export default function AnalyticsPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [analytics, setAnalytics] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/')
      return
    }
    fetchAnalytics()
  }, [isAuthenticated, router])

  const fetchAnalytics = async () => {
    setIsLoading(true)
    try {
      const response = await analyticsAPI.getSkillAnalytics(30, 20)
      setAnalytics(response.data)
    } catch (error) {
      console.error('Error fetching analytics:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (!isAuthenticated) return null

  const topSkillsData = analytics?.top_skills ? {
    labels: analytics.top_skills.slice(0, 10).map((s: any) => s.skill),
    datasets: [
      {
        label: 'Demand Count',
        data: analytics.top_skills.slice(0, 10).map((s: any) => s.demand_count),
        backgroundColor: 'rgba(147, 51, 234, 0.5)',
        borderColor: 'rgba(147, 51, 234, 1)',
        borderWidth: 1,
      },
    ],
  } : null

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">Analytics</h1>
          <p className="text-gray-400 mt-2">Skill demand trends and market insights</p>
        </div>

        {isLoading ? (
          <div className="text-center py-12">
            <p className="text-gray-400">Loading analytics...</p>
          </div>
        ) : analytics ? (
          <>
            <div className="glass-card rounded-xl p-6">
              <h2 className="text-xl font-semibold text-white mb-4">Top Skills by Demand</h2>
              {topSkillsData && (
                <div className="h-64">
                  <Bar data={topSkillsData} options={{ 
                    maintainAspectRatio: false,
                    scales: {
                      x: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: 'rgba(255, 255, 255, 0.6)' }
                      },
                      y: {
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: 'rgba(255, 255, 255, 0.6)' }
                      }
                    },
                    plugins: {
                      legend: { labels: { color: 'rgba(255, 255, 255, 0.8)' } }
                    }
                  }} />
                </div>
              )}
            </div>

            <div className="glass-card rounded-xl p-6">
              <h2 className="text-xl font-semibold text-white mb-4">Top Skills List</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {analytics.top_skills?.slice(0, 15).map((skill: any, idx: number) => (
                  <div key={idx} className="glass rounded-lg p-4 glass-hover">
                    <div className="flex justify-between items-center">
                      <span className="font-medium text-white">{skill.skill}</span>
                      <span className="text-sm text-primary-400 font-semibold">
                        {skill.demand_count}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        ) : (
          <div className="glass-card rounded-xl p-12 text-center">
            <p className="text-gray-400">No analytics data available. Scrape some jobs first.</p>
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}

