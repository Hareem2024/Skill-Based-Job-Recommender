'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import { authAPI } from '@/services/api'
import toast from 'react-hot-toast'

interface RegisterFormData {
  email: string
  password: string
  full_name?: string
}

export default function RegisterForm() {
  const router = useRouter()
  const { login } = useAuthStore()
  const [isLoading, setIsLoading] = useState(false)
  const { register, handleSubmit, formState: { errors } } = useForm<RegisterFormData>()

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true)
    try {
      const registerResponse = await authAPI.register(data)
      
      // Auto-login after registration
      const loginResponse = await authAPI.login(data.email, data.password)
      const { access_token } = loginResponse.data
      
      // Get user info with token
      const userResponse = await authAPI.getMe(access_token)
      const user = userResponse.data
      
      // Store token and user (synchronous update)
      login(access_token, user)
      
      toast.success('Registration successful!')
      
      // Small delay to ensure state propagates, then redirect
      await new Promise(resolve => setTimeout(resolve, 50))
      router.replace('/dashboard')
    } catch (error: any) {
      console.error('Registration error:', error)
      const errorMessage = error.response?.data?.detail || error.message || 'Registration failed. Please check your connection and try again.'
      toast.error(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="full_name" className="block text-sm font-medium text-gray-300 mb-1">
          Full Name (Optional)
        </label>
        <input
          id="full_name"
          type="text"
          {...register('full_name')}
          className="w-full px-4 py-3 glass rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-white bg-transparent placeholder-gray-500"
          placeholder="Enter your full name"
        />
      </div>

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
          {...register('password', { 
            required: 'Password is required',
            minLength: { value: 6, message: 'Password must be at least 6 characters' }
          })}
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
        {isLoading ? 'Registering...' : 'Register'}
      </button>
    </form>
  )
}

