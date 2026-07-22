import { useQuery } from '@tanstack/react-query'
import { mealService } from '../../services'
import LoadingSpinner from '../../components/LoadingSpinner'
import MealCard from '../../components/MealCard'
import { Heart, Calendar } from 'lucide-react'

export default function Favorites() {
  const { data, isLoading } = useQuery({
    queryKey: ['favorites-list'],
    queryFn: () => mealService.getFavorites().then((r) => r.data),
  })

  const favorites = data?.results || data || []

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Favorite Meal Plans</h1>
        <p className="page-subtitle">Your saved recipes and high-performance meal plans</p>
      </div>

      {isLoading && <LoadingSpinner />}

      {!isLoading && favorites.length === 0 && (
        <div className="card text-center py-16 text-slate-500">
          <Heart size={40} className="mx-auto mb-3 opacity-30 text-red-400" />
          <p className="text-sm">No saved favorite meal plans yet. Click the heart icon on any plan to save it here!</p>
        </div>
      )}

      {!isLoading && favorites.length > 0 && (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {favorites.map((fav) => (
            <div key={fav.id} className="card space-y-2">
              <div className="flex items-center justify-between">
                <span className="badge badge-purple text-[10px]">Saved</span>
                <Heart size={16} className="fill-red-400 text-red-400" />
              </div>
              <h3 className="font-semibold text-white text-sm">{fav.meal_plan?.title || 'Saved Meal Plan'}</h3>
              <p className="text-xs text-slate-400">{fav.meal_plan?.target_calories} kcal / day</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
