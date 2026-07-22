import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { healthService } from '../../services'
import LoadingSpinner from '../../components/LoadingSpinner'
import { Droplets, Plus, Minus, Trophy } from 'lucide-react'
import toast from 'react-hot-toast'

export default function WaterTracker() {
  const qc = useQueryClient()

  const { data: water, isLoading } = useQuery({
    queryKey: ['water-today'],
    queryFn: () => healthService.getWater().then((r) => r.data),
  })

  const updateWater = useMutation({
    mutationFn: (amount_ml) => healthService.updateWater({ amount_ml }),
    onSuccess: () => {
      qc.invalidateQueries(['water-today'])
      qc.invalidateQueries(['dashboard'])
      toast.success('Water intake logged!')
    },
  })

  if (isLoading) return <LoadingSpinner />

  const current = water?.amount_ml || 0
  const target = water?.target_ml || 2500
  const pct = Math.min(100, Math.round((current / target) * 100))

  const addAmount = (ml) => {
    updateWater.mutate(Math.max(0, current + ml))
  }

  return (
    <div className="page-container max-w-2xl">
      <div className="page-header">
        <h1 className="page-title">Daily Water Tracker</h1>
        <p className="page-subtitle">Optimal hydration based on your body weight and activity level</p>
      </div>

      <div className="card text-center space-y-6 p-8">
        <div className="w-20 h-20 rounded-full bg-blue-500/10 border-2 border-blue-500/30 flex items-center justify-center mx-auto shadow-glow-teal">
          <Droplets size={36} className="text-blue-400" />
        </div>

        <div>
          <p className="text-5xl font-bold font-display text-white">{current}<span className="text-base text-slate-400 font-normal"> / {target} ml</span></p>
          <p className="text-xs text-blue-400 font-medium mt-1">{pct}% of daily hydration target achieved</p>
        </div>

        {/* Progress bar */}
        <div className="progress-track h-4">
          <div className="progress-bar bg-gradient-to-r from-blue-600 to-cyan-400" style={{ width: `${pct}%` }} />
        </div>

        {/* Quick add buttons */}
        <div className="grid grid-cols-4 gap-3 pt-4 border-t border-surface-border">
          {[
            { label: '+250 ml', val: 250 },
            { label: '+500 ml', val: 500 },
            { label: '+750 ml', val: 750 },
            { label: 'Reset',   val: -current },
          ].map(({ label, val }) => (
            <button
              key={label}
              onClick={() => addAmount(val)}
              className="btn-secondary py-3 text-xs flex flex-col items-center gap-1 font-semibold"
              disabled={updateWater.isPending}
            >
              {label}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
