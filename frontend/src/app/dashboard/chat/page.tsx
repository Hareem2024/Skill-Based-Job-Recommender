'use client'

import { useEffect, useState, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/store/authStore'
import DashboardLayout from '@/components/layout/DashboardLayout'
import { chatAPI } from '@/services/api'
import toast from 'react-hot-toast'
import { Send, Bot, User } from 'lucide-react'

interface Message {
  message: string
  response: string
  created_at: string
}

export default function ChatPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/')
      return
    }
    fetchHistory()
  }, [isAuthenticated, router])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const fetchHistory = async () => {
    try {
      const response = await chatAPI.getHistory(20)
      setMessages(response.data.reverse())
    } catch (error) {
      console.error('Error fetching chat history:', error)
    }
  }

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = input
    setInput('')
    setIsLoading(true)

    // Add user message immediately
    const tempUserMsg: Message = {
      message: userMessage,
      response: '',
      created_at: new Date().toISOString(),
    }
    setMessages((prev) => [...prev, tempUserMsg])

    try {
      const response = await chatAPI.sendMessage(userMessage)
      const botResponse: Message = {
        message: userMessage,
        response: response.data.response,
        created_at: response.data.created_at || new Date().toISOString(),
      }
      setMessages((prev) => [...prev.slice(0, -1), botResponse])
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to send message')
      setMessages((prev) => prev.slice(0, -1))
    } finally {
      setIsLoading(false)
    }
  }

  if (!isAuthenticated) return null

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent">AI Chat Mentor</h1>
          <p className="text-gray-400 mt-2">Ask questions about your career, projects, and learning path</p>
        </div>

        <div className="glass-card rounded-xl flex flex-col shadow-2xl" style={{ height: '600px' }}>
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 ? (
              <div className="text-center text-gray-400 py-12">
                <Bot className="w-12 h-12 mx-auto mb-4 text-primary-400" />
                <p className="text-white">Start a conversation with your AI mentor!</p>
                <p className="text-sm mt-2">Ask about projects, skills to learn, or career advice.</p>
              </div>
            ) : (
              messages.map((msg, idx) => (
                <div key={idx} className="space-y-2">
                  <div className="flex items-start space-x-2">
                    <User className="w-5 h-5 text-primary-400 mt-1" />
                    <div className="flex-1 glass rounded-lg p-3">
                      <p className="text-white">{msg.message}</p>
                    </div>
                  </div>
                  {msg.response && (
                    <div className="flex items-start space-x-2">
                      <Bot className="w-5 h-5 text-green-400 mt-1" />
                      <div className="flex-1 glass rounded-lg p-3 bg-gradient-to-r from-primary-500/10 to-accent-500/10">
                        <p className="text-gray-100">{msg.response}</p>
                      </div>
                    </div>
                  )}
                </div>
              ))
            )}
            {isLoading && (
              <div className="flex items-start space-x-2">
                <Bot className="w-5 h-5 text-green-400 mt-1" />
                <div className="flex-1 glass rounded-lg p-3 bg-gradient-to-r from-primary-500/10 to-accent-500/10">
                  <p className="text-gray-300">Thinking...</p>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSend} className="border-t border-white/10 p-4">
            <div className="flex space-x-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask a question..."
                className="flex-1 px-4 py-2 glass rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-white placeholder-gray-500 bg-transparent"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="px-4 py-2 bg-gradient-to-r from-primary-500 to-accent-500 text-white rounded-lg hover:from-primary-600 hover:to-accent-600 disabled:opacity-50 flex items-center shadow-lg transition-all"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </form>
        </div>
      </div>
    </DashboardLayout>
  )
}

