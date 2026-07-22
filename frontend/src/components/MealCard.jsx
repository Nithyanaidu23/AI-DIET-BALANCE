import { Clock, Flame, Dumbbell, Wheat, Droplets } from 'lucide-react'
import clsx from 'clsx'

const MEAL_TYPE_CONFIG = {
  breakfast:    { label: 'Breakfast',    color: 'text-amber-400',  bg: 'bg-amber-400/10'  },
  lunch:        { label: 'Lunch',        color: 'text-blue-400',   bg: 'bg-blue-400/10'   },
  dinner:       { label: 'Dinner',       color: 'text-purple-400', bg: 'bg-purple-400/10' },
  snack:        { label: 'Snack',        color: 'text-brand-400',  bg: 'bg-brand-400/10'  },
  pre_workout:  { label: 'Pre-Workout',  color: 'text-orange-400', bg: 'bg-orange-400/10' },
  post_workout: { label: 'Post-Workout', color: 'text-teal-400',   bg: 'bg-teal-400/10'   },
}

export default function MealCard({ meal, expanded = false, onToggle }) {
  const cfg = MEAL_TYPE_CONFIG[meal.meal_type] || MEAL_TYPE_CONFIG.snack
  const totalTime = (meal.prep_time_minutes || 0) + (meal.cook_time_minutes || 0)

  return (
    <div className="card hover-lift cursor-pointer animate-in" onClick={onToggle}>
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div>
          <span className={clsx('badge text-xs mb-2', cfg.bg, cfg.color)}>{cfg.label}</span>
          <h3 className="font-semibold text-white text-sm leading-snug">{meal.name}</h3>
          {meal.description && (
            <p className="text-xs text-slate-400 mt-0.5 line-clamp-2">{meal.description}</p>
          )}
        </div>
        {totalTime > 0 && (
          <div className="flex items-center gap-1 text-xs text-slate-500 shrink-0 ml-2">
            <Clock size={12} />
            <span>{totalTime}m</span>
          </div>
        )}
      </div>

      {/* Macro pills */}
      <div className="flex flex-wrap gap-2">
        <div className="macro-pill bg-red-500/10 text-red-400">
          <Flame size={11} /> {meal.calories} kcal
        </div>
        <div className="macro-pill bg-blue-500/10 text-blue-400">
          <Dumbbell size={11} /> {meal.protein_g}g P
        </div>
        <div className="macro-pill bg-amber-500/10 text-amber-400">
          <Wheat size={11} /> {meal.carbs_g}g C
        </div>
        <div className="macro-pill bg-purple-500/10 text-purple-400">
          <Droplets size={11} /> {meal.fat_g}g F
        </div>
      </div>

      {/* Expanded recipe */}
      {expanded && meal.recipe_steps && (
        <div className="mt-4 pt-4 border-t border-surface-border animate-in">
          <p className="text-xs font-semibold text-slate-300 mb-2 uppercase tracking-wider">Recipe</p>
          <p className="text-xs text-slate-400 whitespace-pre-line leading-relaxed">{meal.recipe_steps}</p>
        </div>
      )}
    </div>
  )
}
