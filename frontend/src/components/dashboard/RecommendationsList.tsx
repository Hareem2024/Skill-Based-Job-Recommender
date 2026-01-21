'use client'

import { useEffect, useState } from 'react'
import { recommendationAPI } from '@/services/api'
import { Target, Clock, BookOpen } from 'lucide-react'

export default function RecommendationsList() {
  const [recommendations, setRecommendations] = useState<any[]>([])

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const response = await recommendationAPI.getAll()
        setRecommendations(response.data.slice(0, 5))
      } catch (error) {
        console.error('Error fetching recommendations:', error)
      }
    }

    fetchRecommendations()
  }, [])

  return (
    <div className="glass-card rounded-xl p-6">
      <h2 className="text-xl font-semibold text-white mb-4">Your Recommendations</h2>
      {recommendations.length === 0 ? (
        <p className="text-gray-400">
          Generate recommendations by uploading a resume and creating a roadmap.
        </p>
      ) : (
        <div className="space-y-4">
          {recommendations.map((rec) => (
            <div key={rec.id} className="glass rounded-lg p-4 glass-hover">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <Target className="w-5 h-5 text-primary-400" />
                    <h3 className="font-medium text-white">{rec.title}</h3>
                    <span className="text-xs bg-primary-500/20 text-primary-300 px-2 py-1 rounded border border-primary-500/30">
                      {rec.recommendation_type}
                    </span>
                  </div>
                  <p className="text-sm text-gray-300 mb-2">{rec.description}</p>
                  {rec.estimated_time && (
                    <div className="flex items-center text-xs text-gray-400">
                      <Clock className="w-4 h-4 mr-1" />
                      {rec.estimated_time}
                    </div>
                  )}
                  {rec.resources && rec.resources.length > 0 && (
                    <div className="mt-2 flex items-center text-xs text-gray-400">
                      <BookOpen className="w-4 h-4 mr-1" />
                      {rec.resources.length} resources
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

