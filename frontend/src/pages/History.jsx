import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { mealService } from '../services'
import LoadingSpinner from '../components/LoadingSpinner'
import { Calendar, Heart, HeartOff, Trash2, Download, ChevronRight } from 'lucide-react'
import { Link } from 'react-router-dom'
import { exportPlanToPDF } from '../utils/pdfExport'
import toast from 'react-hot-toast'

function PlanRow({ plan }) {
  const qc = useQueryClient()

  const fav = useMutation({
    mutationFn: () => mealService.toggleFavorite(plan.id),
    onSuccess: () => qc.invalidateQueries(['plans']),
  })
  const del = useMutation({
    mutationFn: () => mealService.deletePlan(plan.id),
    onSuccess: () => { qc.invalidateQueries(['plans']); toast.success('Plan deleted.') },
  })

  return (
    <div className="card hover-lift flex items-start gap-4">
      <div className="w-10 h-10 rounded-xl bg-brand-600/20 flex items-center justify-center shrink-0">
        <Calendar size={18} className="text-brand-400" />
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-start justify-between gap-2 flex-wrap">
          <div>
            <h3 className="font-semibold text-white text-sm">{plan.title}</h3>
            <p className="text-xs text-slate-500 mt-0.5">{plan.start_date} → {plan.end_date}</p>
          </div>
          <div className="flex items-center gap-1.5">
            {plan.ai_generated && <span className="badge badge-green text-[10px]">AI</span>}
            {plan.is_favorited && <span className="badge badge-purple text-[10px]">Saved</span>}
          </div>
        </div>

        <div className="flex flex-wrap gap-3 mt-2 text-xs text-slate-400">
          <span>{plan.target_calories} kcal</span>
          <span>P {plan.target_protein_g}g</span>
          <span>C {plan.target_carbs_g}g</span>
          <span>F {plan.target_fat_g}g</span>
        </div>
      </div>

      <div className="flex items-center gap-1.5 shrink-0">
        <button onClick={() => exportPlanToPDF(plan)} className="btn-icon" title="Download PDF">
          <Download size={14} />
        </button>
        <button onClick={() => fav.mutate()} className="btn-icon" title={plan.is_favorited ? 'Unsave' : 'Save'}>
          {plan.is_favorited
            ? <HeartOff size={14} className="text-red-400" />
            : <Heart size={14} />
          }
        </button>
        <button
          onClick={() => { if (confirm('Delete this plan?')) del.mutate() }}
          className="btn-icon hover:text-red-400"
          title="Delete"
        >
          <Trash2 size={14} />
        </button>
      </div>
    </div>
  )
}

export default function History() {
  const { data, isLoading } = useQuery({
    queryKey: ['plans'],
    queryFn:  () => mealService.getPlans().then((r) => r.data),
  })

  const plans = data?.results || data || []

  return (
    <div className="page-container">
      <div className="page-header flex items-center justify-between">
        <div>
          <h1 className="page-title">Meal History</h1>
          <p className="page-subtitle">{plans.length} meal plan{plans.length !== 1 ? 's' : ''} saved</p>
        </div>
        <Link to="/planner" className="btn-primary text-sm">+ New Plan</Link>
      </div>

      {isLoading && <LoadingSpinner />}

      {!isLoading && plans.length === 0 && (
        <div className="card text-center py-16">
          <Calendar size={40} className="mx-auto mb-3 text-slate-600" />
          <p className="text-slate-400 text-sm mb-4">No meal plans yet</p>
          <Link to="/planner" className="btn-primary text-sm">Generate your first plan</Link>
        </div>
      )}

      <div className="space-y-3">
        {plans.map((plan) => <PlanRow key={plan.id} plan={plan} />)}
      </div>
    </div>
  )
}
