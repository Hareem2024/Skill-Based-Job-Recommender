'use client'

import { useEffect, useState } from 'react'
import { Radar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js'
import { resumeAPI, jobAPI } from '@/services/api'

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend)

export default function SkillMatchChart() {
  const [chartData, setChartData] = useState<any>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const resumesRes = await resumeAPI.getAll()
        const jobsRes = await jobAPI.getAll({ limit: 10 })

        if (resumesRes.data.length > 0 && jobsRes.data.length > 0) {
          const resume = resumesRes.data[0]
          const skills = resume.extracted_skills || []

          // Get top skills from jobs
          const allJobSkills: string[] = []
          jobsRes.data.forEach((job: any) => {
            if (job.required_skills) {
              allJobSkills.push(...job.required_skills)
            }
          })

          // Count skill frequency
          const skillCounts: Record<string, number> = {}
          allJobSkills.forEach((skill) => {
            skillCounts[skill] = (skillCounts[skill] || 0) + 1
          })

          const topSkills = Object.entries(skillCounts)
            .sort(([, a], [, b]) => b - a)
            .slice(0, 8)
            .map(([skill]) => skill)

          const userSkillLevels = topSkills.map((skill) =>
            skills.includes(skill) ? 80 : 20
          )

          setChartData({
            labels: topSkills,
            datasets: [
              {
                label: 'Your Skills',
                data: userSkillLevels,
                backgroundColor: 'rgba(147, 51, 234, 0.2)',
                borderColor: 'rgba(147, 51, 234, 1)',
                borderWidth: 2,
              },
            ],
          })
        }
      } catch (error) {
        console.error('Error fetching chart data:', error)
      }
    }

    fetchData()
  }, [])

  if (!chartData) {
    return (
      <div className="glass-card rounded-xl p-6">
        <h2 className="text-xl font-semibold text-white mb-4">Skill Match Analysis</h2>
        <p className="text-gray-400">Upload a resume to see your skill match</p>
      </div>
    )
  }

  return (
    <div className="glass-card rounded-xl p-6">
      <h2 className="text-xl font-semibold text-white mb-4">Skill Match Analysis</h2>
      <div className="h-64">
        <Radar data={chartData} options={{ 
          maintainAspectRatio: false,
          scales: {
            r: {
              grid: { color: 'rgba(255, 255, 255, 0.1)' },
              ticks: { color: 'rgba(255, 255, 255, 0.6)' },
              pointLabels: { color: 'rgba(255, 255, 255, 0.8)' }
            }
          },
          plugins: {
            legend: { labels: { color: 'rgba(255, 255, 255, 0.8)' } }
          }
        }} />
      </div>
    </div>
  )
}

