'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import DashboardLayout from '@/components/layout/DashboardLayout'
import StatsCards from '@/components/dashboard/StatsCards'
import SkillMatchChart from '@/components/dashboard/SkillMatchChart'
import RecentJobs from '@/components/dashboard/RecentJobs'
import RecommendationsList from '@/components/dashboard/RecommendationsList'

export default function DashboardPage() {
  const router = useRouter()
  const { isAuthenticated, token } = useAuthStore()
  const [isChecking, setIsChecking] = useState(true)

  useEffect(() => {
    // Wait a moment for Zustand persist to hydrate
    const timer = setTimeout(() => {
      setIsChecking(false)
      if (!isAuthenticated && !token) {
        router.replace('/')
      }
    }, 100)

    return () => clearTimeout(timer)
  }, [isAuthenticated, token, router])

  if (isChecking) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black">
        <div className="text-gray-400">Loading...</div>
      </div>
    )
  }

  if (!isAuthenticated && !token) {
    return null
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">Dashboard</h1>
          <p className="text-gray-400 mt-2">Welcome back! Here's your overview.</p>
        </div>

        <StatsCards />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <SkillMatchChart />
          <RecentJobs />
        </div>

        <RecommendationsList />
      </div>
    </DashboardLayout>
  )
}

