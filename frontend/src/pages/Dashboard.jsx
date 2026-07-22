import { useQuery } from '@tanstack/react-query'
import { healthService } from '../services'
import LoadingSpinner from '../components/LoadingSpinner'
import NutritionChart from '../components/NutritionChart'
import MealCard from '../components/MealCard'
import { Flame, Droplets, Scale, Trophy, TrendingUp, Calendar, ChevronRight } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { Link } from 'react-router-dom'
import { useState } from 'react'

function KpiCard({ icon: Icon, label, value, unit, color = 'brand' }) {
  const colors = {
    brand:  { bg: 'bg-brand-500/10',  text: 'text-brand-400',  icon: 'bg-brand-500/20'  },
    blue:   { bg: 'bg-blue-500/10',   text: 'text-blue-400',   icon: 'bg-blue-500/20'   },
    purple: { bg: 'bg-purple-500/10', text: 'text-purple-400', icon: 'bg-purple-500/20' },
    amber:  { bg: 'bg-amber-500/10',  text: 'text-amber-400',  icon: 'bg-amber-500/20'  },
  }
  const c = colors[color] || colors.brand

  return (
    <div className={`kpi-card ${c.bg}`}>
      <div className="flex items-center gap-3">
        <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 ${c.icon}`}>
          <Icon size={18} className={c.text} />
        </div>
        <div className="min-w-0 flex-1">
          <p className="kpi-label">{label}</p>
          <p className="kpi-value">
            {value ?? '—'}
            {unit && <span className="text-sm font-normal text-slate-400 ml-1">{unit}</span>}
          </p>
        </div>
      </div>
    </div>
  )
}

function ProgressBar({ label, current, target, color }) {
  const pct = target > 0 ? Math.min(100, Math.round((current / target) * 100)) : 0
  const colors = { brand: 'from-brand-500 to-accent-500', blue: 'from-blue-500 to-cyan-400', amber: 'from-amber-500 to-orange-400', purple: 'from-purple-500 to-pink-400' }

  return (
    <div>
      <div className="flex justify-between text-xs mb-1.5">
        <span className="text-slate-400">{label}</span>
        <span className="text-slate-300 font-medium">{current}<span className="text-slate-500">/{target}</span></span>
      </div>
      <div className="progress-track">
        <div
          className={`progress-bar bg-gradient-to-r ${colors[color] || colors.brand}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [expandedMeal, setExpandedMeal] = useState(null)

  const { data: dash, isLoading, error } = useQuery({
    queryKey: ['dashboard'],
    queryFn:  () => healthService.getDashboard().then((r) => r.data),
    refetchInterval: 60_000,
  })

  if (isLoading) return <LoadingSpinner label="Loading dashboard…" />
  if (error) return (
    <div className="page-container">
      <div className="card text-center text-red-400 py-12">
        Failed to load dashboard. <button onClick={() => window.location.reload()} className="underline ml-1">Retry</button>
      </div>
    </div>
  )

  const bmi   = dash?.latest_bmi
  const water = dash?.water_today
  const plan  = dash?.latest_meal_plan
  const trend = dash?.bmi_trend || []
  const todayMeals = plan?.meals?.filter((m) => m.day_number === 1) || []

  // Macro totals from today's meals
  const macros = todayMeals.reduce((acc, m) => ({
    calories: acc.calories + (m.calories || 0),
    protein:  acc.protein  + parseFloat(m.protein_g  || 0),
    carbs:    acc.carbs    + parseFloat(m.carbs_g    || 0),
    fat:      acc.fat      + parseFloat(m.fat_g      || 0),
  }), { calories: 0, protein: 0, carbs: 0, fat: 0 })

  const targetCal = plan?.target_calories || 2000

  return (
    <div className="page-container space-y-6">
      {/* Header */}
      <div className="page-header flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="page-title">
            Good {new Date().getHours() < 12 ? 'morning' : new Date().getHours() < 18 ? 'afternoon' : 'evening'},
            {' '}<span className="text-gradient">{dash?.user?.full_name?.split(' ')[0] || 'there'}</span> 👋
          </h1>
          <p className="page-subtitle">Here&apos;s your nutrition overview for today</p>
        </div>
        <Link to="/planner" className="btn-primary gap-2 w-full sm:w-auto">
          <Calendar size={15} /> Generate Plan
        </Link>
      </div>

      {/* KPI Row (Mobile 1 col, Tablet 2 col, Laptop/Desktop 4 col) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <KpiCard icon={Flame}   label="Calories Today"  value={macros.calories}  unit="kcal"   color="brand" />
        <KpiCard icon={Droplets}label="Water Today"    value={water ? Math.round(water.amount_ml / 1000 * 10) / 10 : 0} unit="L" color="blue" />
        <KpiCard icon={Scale}   label="Current BMI"    value={bmi?.bmi || '—'}                               color="purple" />
        <KpiCard icon={Trophy}  label="Total Plans"    value={dash?.total_plans ?? 0}                         color="amber" />
      </div>

      {/* Progress + Chart row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Macro progress */}
        <div className="card lg:col-span-1">
          <h2 className="text-sm font-semibold text-white mb-4">Today&apos;s Macros</h2>
          <div className="space-y-4">
            <ProgressBar label="Calories" current={macros.calories} target={targetCal}           color="brand"  />
            <ProgressBar label="Protein"  current={Math.round(macros.protein)}  target={plan?.target_protein_g || 150} color="blue"   />
            <ProgressBar label="Carbs"    current={Math.round(macros.carbs)}    target={plan?.target_carbs_g   || 200} color="amber"  />
            <ProgressBar label="Fat"      current={Math.round(macros.fat)}      target={plan?.target_fat_g     || 65}  color="purple" />
          </div>
        </div>

        {/* Doughnut chart */}
        <div className="card flex flex-col justify-center items-center text-center">
          <h2 className="text-sm font-semibold text-white mb-2 w-full text-left">Macro Breakdown</h2>
          {macros.protein + macros.carbs + macros.fat > 0 ? (
            <div className="w-full flex items-center justify-center">
              <NutritionChart protein={macros.protein} carbs={macros.carbs} fat={macros.fat} size={200} />
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-slate-500 text-sm py-8">
              No meal data yet — generate a plan!
            </div>
          )}
        </div>

        {/* BMI trend */}
        <div className="card">
          <h2 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
            <TrendingUp size={14} className="text-brand-400" /> Weight Trend
          </h2>
          {trend.length > 1 ? (
            <div className="w-full h-44">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trend}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="recorded_at__date" tick={{ fontSize: 10, fill: '#64748b' }} tickLine={false} />
                  <YAxis domain={['auto', 'auto']} tick={{ fontSize: 10, fill: '#64748b' }} tickLine={false} axisLine={false} />
                  <Tooltip
                    contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8, fontSize: 12 }}
                    labelStyle={{ color: '#94a3b8' }}
                  />
                  <Line type="monotone" dataKey="weight_kg" stroke="#22c55e" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="text-center text-slate-500 text-xs py-8">
              Log your BMI to see trends
              <br />
              <Link to="/bmi" className="text-brand-400 hover:underline mt-1 inline-block">Go to BMI Calculator</Link>
            </div>
          )}
        </div>
      </div>

      {/* Today's meals */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-semibold text-white">Today&apos;s Meals</h2>
          <Link to="/history" className="text-xs text-brand-400 hover:text-brand-300 flex items-center gap-1">
            View all <ChevronRight size={12} />
          </Link>
        </div>

        {todayMeals.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
            {todayMeals.map((meal) => (
              <MealCard
                key={meal.id}
                meal={meal}
                expanded={expandedMeal === meal.id}
                onToggle={() => setExpandedMeal((id) => id === meal.id ? null : meal.id)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-slate-500">
            <Calendar size={32} className="mx-auto mb-3 opacity-30" />
            <p className="text-sm mb-4">No meal plan yet</p>
            <Link to="/planner" className="btn-primary text-sm">Generate AI Meal Plan</Link>
          </div>
        )}
      </div>
    </div>
  )
}
