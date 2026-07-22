import { useQuery } from '@tanstack/react-query'
import { mealService, exportService } from '../../services'
import LoadingSpinner from '../../components/LoadingSpinner'
import { Download, Calendar } from 'lucide-react'
import { exportPlanToPDF } from '../../utils/pdfExport'

export default function AdminMealPlans() {
  const { data, isLoading } = useQuery({
    queryKey: ['admin-meal-plans'],
    queryFn: () => mealService.getPlans().then((r) => r.data),
  })

  const plans = data?.results || data || []

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold font-display text-white">Platform Meal Plans</h1>
          <p className="text-xs text-slate-400">All user generated 7-day meal plans and nutritional targets</p>
        </div>
        <button
          onClick={() => exportService.downloadFile('meal_plans.csv')}
          className="btn-secondary text-xs gap-1.5"
        >
          <Download size={13} /> Export CSV
        </button>
      </div>

      {isLoading && <LoadingSpinner />}

      {!isLoading && (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="border-b border-slate-800 text-slate-400 uppercase tracking-wider bg-slate-900/50">
                <tr>
                  <th className="py-3 px-4">Plan Title</th>
                  <th className="py-3 px-4">User</th>
                  <th className="py-3 px-4">Duration</th>
                  <th className="py-3 px-4">Target Cal</th>
                  <th className="py-3 px-4">Macros (P/C/F)</th>
                  <th className="py-3 px-4 text-right">PDF</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50 text-slate-300">
                {plans.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-800/30">
                    <td className="py-3 px-4 font-semibold text-white">{p.title}</td>
                    <td className="py-3 px-4 text-slate-400">{p.user_email || 'User'}</td>
                    <td className="py-3 px-4 text-slate-500">{p.start_date} → {p.end_date}</td>
                    <td className="py-3 px-4 text-emerald-400 font-bold">{p.target_calories} kcal</td>
                    <td className="py-3 px-4 text-slate-400">
                      {p.target_protein_g}g / {p.target_carbs_g}g / {p.target_fat_g}g
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button onClick={() => exportPlanToPDF(p)} className="btn-icon">
                        <Download size={13} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
