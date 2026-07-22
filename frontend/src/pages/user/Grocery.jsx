import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { mealService } from '../../services'
import LoadingSpinner from '../../components/LoadingSpinner'
import { ShoppingCart, Check, Download } from 'lucide-react'

export default function Grocery() {
  const [checkedItems, setCheckedItems] = useState({})

  const { data: plansData, isLoading } = useQuery({
    queryKey: ['plans-grocery'],
    queryFn: () => mealService.getPlans().then((r) => r.data),
  })

  const latestPlan = plansData?.results?.[0] || plansData?.[0]

  const { data: groceryData } = useQuery({
    queryKey: ['grocery-items', latestPlan?.id],
    queryFn: () => mealService.getGrocery(latestPlan.id).then((r) => r.data),
    enabled: !!latestPlan?.id,
  })

  const items = groceryData || []

  const toggleCheck = (id) => {
    setCheckedItems((prev) => ({ ...prev, [id]: !prev[id] }))
  }

  // Group by category
  const categories = items.reduce((acc, item) => {
    const cat = item.category || 'General'
    if (!acc[cat]) acc[cat] = []
    acc[cat].push(item)
    return acc
  }, {})

  return (
    <div className="page-container max-w-4xl">
      <div className="page-header flex justify-between items-center flex-wrap gap-4">
        <div>
          <h1 className="page-title">Grocery Shopping List</h1>
          <p className="page-subtitle">Auto-generated ingredient checklist for your current meal plan</p>
        </div>
      </div>

      {isLoading && <LoadingSpinner />}

      {!isLoading && items.length === 0 && (
        <div className="card text-center py-16 text-slate-500">
          <ShoppingCart size={40} className="mx-auto mb-3 opacity-30" />
          <p>No active grocery list. Generate a meal plan to build your list automatically!</p>
        </div>
      )}

      {!isLoading && items.length > 0 && (
        <div className="space-y-6 animate-in">
          {Object.entries(categories).map(([cat, catItems]) => (
            <div key={cat} className="card">
              <h2 className="text-xs font-semibold uppercase tracking-wider text-brand-400 mb-3">{cat}</h2>
              <div className="space-y-2">
                {catItems.map((item) => {
                  const isChecked = !!checkedItems[item.id]
                  return (
                    <div
                      key={item.id}
                      onClick={() => toggleCheck(item.id)}
                      className={`flex items-center justify-between p-3 rounded-xl border transition-all cursor-pointer ${
                        isChecked ? 'bg-surface/40 border-surface-border text-slate-500 line-through' : 'bg-surface border-surface-border/60 text-slate-200 hover:border-brand-500/50'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`w-5 h-5 rounded-md border flex items-center justify-center transition-colors ${isChecked ? 'bg-brand-500 border-brand-500 text-white' : 'border-slate-600'}`}>
                          {isChecked && <Check size={12} />}
                        </div>
                        <span className="text-sm font-medium">{item.name}</span>
                      </div>
                      <span className="text-xs text-slate-400 font-mono">{item.quantity} {item.unit}</span>
                    </div>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
