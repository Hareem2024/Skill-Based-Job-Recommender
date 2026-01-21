'use client'

import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import Link from 'next/link'
import { 
  LayoutDashboard, 
  FileText, 
  Briefcase, 
  TrendingUp, 
  MessageSquare, 
  LogOut,
  User
} from 'lucide-react'

interface DashboardLayoutProps {
  children: React.ReactNode
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const router = useRouter()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    router.push('/')
  }

  const navItems = [
    { href: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { href: '/dashboard/resumes', icon: FileText, label: 'Resumes' },
    { href: '/dashboard/jobs', icon: Briefcase, label: 'Jobs' },
    { href: '/dashboard/analytics', icon: TrendingUp, label: 'Analytics' },
    { href: '/dashboard/chat', icon: MessageSquare, label: 'AI Chat' },
  ]

  return (
    <div className="min-h-screen bg-black">
      <nav className="glass sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <h1 className="text-xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">
                  Hiring Portal
                </h1>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                {navItems.map((item) => {
                  const Icon = item.icon
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-300 hover:text-white glass-hover rounded-lg transition-colors"
                    >
                      <Icon className="w-4 h-4 mr-2" />
                      {item.label}
                    </Link>
                  )
                })}
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center text-sm text-gray-300 glass px-4 py-2 rounded-lg">
                <User className="w-4 h-4 mr-2 text-primary-400" />
                {user?.full_name || user?.email}
              </div>
              <button
                onClick={handleLogout}
                className="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-300 hover:text-red-400 glass-hover rounded-lg transition-colors"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  )
}

