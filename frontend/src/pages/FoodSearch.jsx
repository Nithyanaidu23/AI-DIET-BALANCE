import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { nutritionService } from '../services'
import LoadingSpinner from '../components/LoadingSpinner'
import { Search, Filter } from 'lucide-react'

const CATEGORIES = [
  { value: '',          label: 'All Categories'  },
  { value: 'grains',   label: 'Grains'           },
  { value: 'protein',  label: 'Protein'          },
  { value: 'dairy',    label: 'Dairy & Eggs'     },
  { value: 'vegetables',label: 'Vegetables'      },
  { value: 'fruits',   label: 'Fruits'           },
  { value: 'legumes',  label: 'Legumes'          },
  { value: 'nuts_seeds',label: 'Nuts & Seeds'    },
  { value: 'fats_oils',label: 'Fats & Oils'      },
  { value: 'beverages',label: 'Beverages'        },
]

function MacroBar({ value, max, color }) {
  const pct = Math.min(100, Math.round((value / max) * 100))
  return (
    <div className="h-1 bg-surface rounded-full overflow-hidden">
      <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
    </div>
  )
}

function FoodCard({ food }) {
  return (
    <div className="card hover-lift text-sm">
      <div className="flex items-start justify-between mb-3">
        <div>
          <p className="font-semibold text-white text-sm">{food.name}</p>
          <p className="text-xs text-slate-500">{food.serving_description || `${food.serving_size_g}g`}</p>
        </div>
        <span className="badge badge-green text-[10px]">{food.category.replace('_', ' ')}</span>
      </div>

      <div className="text-2xl font-bold text-white mb-3">
        {Math.round(food.nutrition_per_serving?.calories || food.calories)} <span className="text-sm font-normal text-slate-400">kcal</span>
      </div>

      <div className="space-y-1.5 text-xs">
        <div className="flex justify-between text-slate-400">
          <span>Protein</span><span className="text-blue-400 font-medium">{parseFloat(food.protein_g).toFixed(1)}g</span>
        </div>
        <MacroBar value={parseFloat(food.protein_g)} max={50} color="bg-blue-500" />

        <div className="flex justify-between text-slate-400 mt-1">
          <span>Carbs</span><span className="text-amber-400 font-medium">{parseFloat(food.carbs_g).toFixed(1)}g</span>
        </div>
        <MacroBar value={parseFloat(food.carbs_g)} max={80} color="bg-amber-500" />

        <div className="flex justify-between text-slate-400 mt-1">
          <span>Fat</span><span className="text-purple-400 font-medium">{parseFloat(food.fat_g).toFixed(1)}g</span>
        </div>
        <MacroBar value={parseFloat(food.fat_g)} max={40} color="bg-purple-500" />

        {parseFloat(food.fiber_g) > 0 && (
          <div className="flex justify-between text-slate-500 mt-1">
            <span>Fiber</span><span>{parseFloat(food.fiber_g).toFixed(1)}g</span>
          </div>
        )}
      </div>

      <div className="flex flex-wrap gap-1.5 mt-3">
        {food.is_vegan && <span className="badge badge-green text-[9px]">Vegan</span>}
        {!food.is_vegan && food.is_vegetarian && <span className="badge badge-blue text-[9px]">Veg</span>}
        {food.is_gluten_free && <span className="badge badge-orange text-[9px]">GF</span>}
      </div>
    </div>
  )
}

export default function FoodSearch() {
  const [search, setSearch]   = useState('')
  const [category, setCategory] = useState('')
  const [vegOnly, setVegOnly] = useState(false)

  const { data, isLoading } = useQuery({
    queryKey: ['foods', search, category, vegOnly],
    queryFn: () => nutritionService.getFoods({
      search: search || undefined,
      category: category || undefined,
      is_vegetarian: vegOnly || undefined,
      page_size: 60,
    }).then((r) => r.data),
    keepPreviousData: true,
  })

  const foods = data?.results || data || []

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Food Database</h1>
        <p className="page-subtitle">Browse {data?.count || '60+'} foods with verified nutritional data</p>
      </div>

      {/* Search & filters */}
      <div className="card mb-6 flex flex-wrap gap-4">
        <div className="flex-1 min-w-48 relative">
          <Search size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input pl-10 py-2 text-sm"
            placeholder="Search foods…"
            id="food-search"
          />
        </div>

        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="select text-sm py-2 w-48"
          id="category-filter"
        >
          {CATEGORIES.map((c) => <option key={c.value} value={c.value}>{c.label}</option>)}
        </select>

        <label className="flex items-center gap-2 text-sm text-slate-300 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={vegOnly}
            onChange={(e) => setVegOnly(e.target.checked)}
            className="w-4 h-4 rounded accent-brand-500"
            id="veg-filter"
          />
          Vegetarian only
        </label>
      </div>

      {isLoading && <LoadingSpinner />}

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {foods.map((f) => <FoodCard key={f.id} food={f} />)}
      </div>

      {!isLoading && foods.length === 0 && (
        <div className="card text-center py-12 text-slate-500">
          <p>No foods found. Try adjusting your search.</p>
        </div>
      )}
    </div>
  )
}
