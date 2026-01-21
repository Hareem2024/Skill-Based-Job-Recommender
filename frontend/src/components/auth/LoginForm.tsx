'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import { authAPI } from '@/services/api'
import toast from 'react-hot-toast'

interface LoginFormData {
  email: string
  password: string
}

export default function LoginForm() {
  const router = useRouter()
  const { login } = useAuthStore()
  const [isLoading, setIsLoading] = useState(false)
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>()

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true)
    try {
      const response = await authAPI.login(data.email, data.password)
      const { access_token } = response.data
      
      // Get user info with token
      const userResponse = await authAPI.getMe(access_token)
      const user = userResponse.data
      
      // Store token and user (synchronous update)
      login(access_token, user)
      
      toast.success('Login successful!')
      
      // Small delay to ensure state propagates, then redirect
      await new Promise(resolve => setTimeout(resolve, 50))
      router.replace('/dashboard')
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Login failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-1">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...register('email', { required: 'Email is required' })}
          className="w-full px-4 py-3 glass rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-white bg-transparent placeholder-gray-500"
          placeholder="Enter your email"
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-400">{errors.email.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-1">
          Password
        </label>
        <input
          id="password"
          type="password"
          {...register('password', { required: 'Password is required' })}
          className="w-full px-4 py-3 glass rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-white bg-transparent placeholder-gray-500"
          placeholder="Enter your password"
        />
        {errors.password && (
          <p className="mt-1 text-sm text-red-400">{errors.password.message}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-gradient-to-r from-primary-500 to-accent-500 text-white py-3 px-4 rounded-lg hover:from-primary-600 hover:to-accent-600 focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:opacity-50 shadow-lg transition-all transform hover:scale-[1.02]"
      >
        {isLoading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  )
}

