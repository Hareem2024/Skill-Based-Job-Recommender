'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import LoginForm from '@/components/auth/LoginForm'
import RegisterForm from '@/components/auth/RegisterForm'
import { useState } from 'react'

export default function Home() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [isLogin, setIsLogin] = useState(true)

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard')
    }
  }, [isAuthenticated, router])

  return (
    <main className="min-h-screen flex items-center justify-center">
      <div className="w-full max-w-md p-8 glass-card rounded-2xl shadow-2xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent mb-2">
            Intelligent Developer Hiring Portal
          </h1>
          <p className="text-gray-400">
            AI-powered job matching and learning roadmap
          </p>
        </div>

        <div className="flex mb-6 glass rounded-lg p-1">
          <button
            onClick={() => setIsLogin(true)}
            className={`flex-1 py-2 px-4 text-center font-medium rounded-md transition-all ${
              isLogin
                ? 'bg-gradient-to-r from-primary-500 to-accent-500 text-white shadow-lg'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            Login
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`flex-1 py-2 px-4 text-center font-medium rounded-md transition-all ${
              !isLogin
                ? 'bg-gradient-to-r from-primary-500 to-accent-500 text-white shadow-lg'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            Register
          </button>
        </div>

        {isLogin ? <LoginForm /> : <RegisterForm />}
      </div>
    </main>
  )
}

