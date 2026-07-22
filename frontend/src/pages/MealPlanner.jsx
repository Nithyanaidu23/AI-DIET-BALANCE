import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { mealService } from '../services'
import MealCard from '../components/MealCard'
import NutritionChart from '../components/NutritionChart'
import LoadingSpinner from '../components/LoadingSpinner'
import toast from 'react-hot-toast'
import { Sparkles, Download, Heart, ShoppingCart, ChevronDown } from 'lucide-react'
import { exportPlanToPDF } from '../utils/pdfExport'

const GOALS = [
  { value: 'lose_fat',          label: 'Lose Fat'            },
  { value: 'build_muscle',      label: 'Build Muscle'        },
  { value: 'maintain',          label: 'Maintain Weight'     },
  { value: 'improve_health',    label: 'Improve Health'      },
  { value: 'increase_endurance',label: 'Increase Endurance'  },
]
const ACTIVITY = [
  { value: 'sedentary', label: 'Sedentary (no exercise)'   },
  { value: 'light',     label: 'Lightly Active (1-3x/wk)'  },
  { value: 'moderate',  label: 'Moderately Active (3-5x/wk)'},
  { value: 'very',      label: 'Very Active (6-7x/wk)'     },
  { value: 'extra',     label: 'Extra Active (2x/day)'      },
]
const PREFS = [
  { value: 'none',         label: 'No Preference'  },
  { value: 'vegetarian',   label: 'Vegetarian'      },
  { value: 'vegan',        label: 'Vegan'           },
  { value: 'pescatarian',  label: 'Pescatarian'     },
  { value: 'keto',         label: 'Keto'            },
  { value: 'gluten_free',  label: 'Gluten-Free'     },
]

export default function MealPlanner() {
  const [result, setResult]           = useState(null)
  const [activeDay, setActiveDay]     = useState(1)
  const [expandedMeal, setExpandedMeal] = useState(null)
  const [showGrocery, setShowGrocery] = useState(false)
  const qc = useQueryClient()

  const { register, handleSubmit, formState: { errors } } = useForm({
    defaultValues: { goal: 'lose_fat', activity_level: 'moderate', food_preference: 'none', age: 25, weight_kg: 70, height_cm: 170, gender: 'male' },
  })

  const generate = useMutation({
    mutationFn: (data) => mealService.generatePlan(data).then((r) => r.data),
    onSuccess: (data) => {
      setResult(data)
      setActiveDay(1)
      qc.invalidateQueries(['dashboard'])
      toast.success('Meal plan generated! 🎉')
    },
    onError: (err) => {
      toast.error(err.response?.data?.error || 'Generation failed. Check your Gemini API key.')
    },
  })

  const favorite = useMutation({
    mutationFn: (id) => mealService.toggleFavorite(id),
    onSuccess: (d) => toast.success(d.data.message),
  })

  const plan = result?.meal_plan
  const health = result?.health_report
  const currentDay = plan?.meals?.filter((m) => m.day_number === activeDay) || []
  const grocery = plan?.grocery_items || []

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">AI Meal Planner</h1>
        <p className="page-subtitle">Generate a personalised 7-day meal plan powered by Gemini AI</p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Form */}
        <div className="lg:col-span-1">
          <form onSubmit={handleSubmit((d) => generate.mutate(d))} className="card space-y-4">
            <h2 className="font-semibold text-white text-sm">Your Details</h2>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="input-label text-xs">Age</label>
                <input {...register('age', { required: true, min: 10, max: 100 })} type="number" className="input py-2 text-sm" placeholder="25" />
              </div>
              <div>
                <label className="input-label text-xs">Gender</label>
                <select {...register('gender')} className="select py-2 text-sm">
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <label className="input-label text-xs">Weight (kg)</label>
                <input {...register('weight_kg', { required: true })} type="number" step="0.1" className="input py-2 text-sm" placeholder="70" />
              </div>
              <div>
                <label className="input-label text-xs">Height (cm)</label>
                <input {...register('height_cm', { required: true })} type="number" className="input py-2 text-sm" placeholder="170" />
              </div>
            </div>

            <div>
              <label className="input-label text-xs">Fitness Goal</label>
              <select {...register('goal')} className="select text-sm py-2">
                {GOALS.map((g) => <option key={g.value} value={g.value}>{g.label}</option>)}
              </select>
            </div>
            <div>
              <label className="input-label text-xs">Activity Level</label>
              <select {...register('activity_level')} className="select text-sm py-2">
                {ACTIVITY.map((a) => <option key={a.value} value={a.value}>{a.label}</option>)}
              </select>
            </div>
            <div>
              <label className="input-label text-xs">Food Preference</label>
              <select {...register('food_preference')} className="select text-sm py-2">
                {PREFS.map((p) => <option key={p.value} value={p.value}>{p.label}</option>)}
              </select>
            </div>
            <div>
              <label className="input-label text-xs">Allergies (comma-separated)</label>
              <input {...register('allergies')} className="input py-2 text-sm" placeholder="peanuts, shellfish" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="input-label text-xs">Country</label>
                <input {...register('country')} className="input py-2 text-sm" placeholder="India" />
              </div>
              <div>
                <label className="input-label text-xs">Budget/day ($)</label>
                <input {...register('budget_per_day_usd')} type="number" className="input py-2 text-sm" placeholder="15" />
              </div>
            </div>

            <button type="submit" className="btn-primary w-full py-2.5" disabled={generate.isPending}>
              {generate.isPending ? (
                <span className="flex items-center gap-2"><span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />Generating…</span>
              ) : (
                <span className="flex items-center gap-2"><Sparkles size={15} />Generate 7-Day Plan</span>
              )}
            </button>
          </form>

          {/* Health report card */}
          {health && (
            <div className="card mt-4 animate-in space-y-2">
              <h3 className="text-xs font-semibold text-white uppercase tracking-wider mb-3">Your Health Report</h3>
              {[
                { label: 'BMI',            value: `${health.bmi} (${health.bmi_category})` },
                { label: 'Goal Calories',  value: `${health.goal_calories} kcal/day` },
                { label: 'BMR',            value: `${health.bmr} kcal` },
                { label: 'TDEE',           value: `${health.tdee} kcal` },
                { label: 'Protein Target', value: `${health.protein_g}g` },
                { label: 'Carbs Target',   value: `${health.carbs_g}g` },
                { label: 'Fat Target',     value: `${health.fat_g}g` },
                { label: 'Water Target',   value: `${Math.round(health.water_intake_ml / 1000 * 10) / 10}L` },
                { label: 'Ideal Weight',   value: `${health.ideal_weight_kg} kg` },
                { label: 'Body Fat Est.',  value: `${health.body_fat_percent}%` },
              ].map(({ label, value }) => (
                <div key={label} className="flex justify-between text-xs">
                  <span className="text-slate-400">{label}</span>
                  <span className="text-slate-200 font-medium">{value}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Results */}
        <div className="lg:col-span-2">
          {generate.isPending && (
            <div className="card flex flex-col items-center justify-center py-20 animate-in">
              <LoadingSpinner size="lg" label="Gemini is crafting your meal plan…" />
              <p className="text-xs text-slate-500 mt-4">This may take 10–20 seconds</p>
            </div>
          )}

          {plan && !generate.isPending && (
            <div className="space-y-4 animate-in">
              {/* Plan header */}
              <div className="card">
                <div className="flex items-start justify-between gap-4 flex-wrap">
                  <div>
                    <h2 className="font-bold text-white text-lg">{plan.title}</h2>
                    <p className="text-xs text-slate-400 mt-0.5">
                      {plan.start_date} → {plan.end_date} · {plan.target_calories} kcal/day
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <button onClick={() => favorite.mutate(plan.id)} className="btn-secondary text-xs py-1.5 px-3 gap-1.5">
                      <Heart size={13} className={plan.is_favorited ? 'fill-red-400 text-red-400' : ''} />
                      Save
                    </button>
                    <button onClick={() => exportPlanToPDF(plan)} className="btn-secondary text-xs py-1.5 px-3 gap-1.5">
                      <Download size={13} /> PDF
                    </button>
                  </div>
                </div>

                <div className="mt-4">
                  <NutritionChart protein={plan.target_protein_g} carbs={plan.target_carbs_g} fat={plan.target_fat_g} size={160} />
                </div>
              </div>

              {/* Day tabs */}
              <div className="card">
                <div className="flex gap-1.5 flex-wrap mb-4">
                  {Array.from({ length: 7 }, (_, i) => i + 1).map((d) => (
                    <button
                      key={d}
                      onClick={() => setActiveDay(d)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${activeDay === d ? 'bg-brand-500 text-white' : 'bg-surface text-slate-400 hover:text-white'}`}
                    >
                      Day {d}
                    </button>
                  ))}
                </div>

                <div className="grid sm:grid-cols-2 gap-3">
                  {currentDay.map((meal) => (
                    <MealCard
                      key={meal.id}
                      meal={meal}
                      expanded={expandedMeal === meal.id}
                      onToggle={() => setExpandedMeal((id) => id === meal.id ? null : meal.id)}
                    />
                  ))}
                </div>
              </div>

              {/* Grocery list toggle */}
              <div className="card">
                <button
                  onClick={() => setShowGrocery((v) => !v)}
                  className="flex items-center justify-between w-full text-sm font-semibold text-white"
                >
                  <span className="flex items-center gap-2"><ShoppingCart size={15} className="text-brand-400" /> Grocery List ({grocery.length} items)</span>
                  <ChevronDown size={14} className={`transition-transform ${showGrocery ? 'rotate-180' : ''}`} />
                </button>

                {showGrocery && (
                  <div className="mt-4 grid sm:grid-cols-2 lg:grid-cols-3 gap-2 animate-in">
                    {grocery.map((item) => (
                      <div key={item.id} className="flex items-center gap-2 text-xs bg-surface rounded-lg px-3 py-2">
                        <span className="text-slate-300 flex-1">{item.name}</span>
                        <span className="text-slate-500">{item.quantity} {item.unit}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {!plan && !generate.isPending && (
            <div className="card flex flex-col items-center justify-center py-20 text-center">
              <Sparkles size={40} className="text-brand-500/40 mb-4" />
              <p className="text-slate-400 text-sm mb-1">Fill in your details and click</p>
              <p className="font-semibold text-white">&ldquo;Generate 7-Day Plan&rdquo;</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
