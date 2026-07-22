import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { nutritionService, exportService } from '../../services'
import LoadingSpinner from '../../components/LoadingSpinner'
import { Search, Download } from 'lucide-react'

export default function AdminFoods() {
  const [search, setSearch] = useState('')

  const { data, isLoading } = useQuery({
    queryKey: ['admin-foods', search],
    queryFn: () => nutritionService.getFoods({ search: search || undefined, page_size: 100 }).then((r) => r.data),
  })

  const foods = data?.results || data || []

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold font-display text-white">Food Database Manager</h1>
          <p className="text-xs text-slate-400">Manage verified nutritional items, macros, and CSV exports</p>
        </div>

        <div className="flex gap-2 w-full sm:w-auto">
          <button
            onClick={() => exportService.downloadFile('foods.csv')}
            className="btn-secondary text-xs gap-1.5 w-full sm:w-auto"
          >
            <Download size={13} /> Export CSV
          </button>
        </div>
      </div>

      <div className="card flex gap-4">
        <div className="flex-1 relative">
          <Search size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input pl-10 py-2 text-sm"
            placeholder="Search foods in database…"
          />
        </div>
      </div>

      {isLoading && <LoadingSpinner />}

      {!isLoading && (
        <div className="table-container">
          <table className="w-full text-left text-xs min-w-[600px]">
            <thead className="border-b border-slate-800 text-slate-400 uppercase tracking-wider bg-slate-900/50">
              <tr>
                <th className="py-3 px-4">Food Name</th>
                <th className="py-3 px-4">Category</th>
                <th className="py-3 px-4">Calories</th>
                <th className="py-3 px-4">Protein</th>
                <th className="py-3 px-4">Carbs</th>
                <th className="py-3 px-4">Fat</th>
                <th className="py-3 px-4">Diet Tags</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50 text-slate-300">
              {foods.map((f) => (
                <tr key={f.id} className="hover:bg-slate-800/30">
                  <td className="py-3 px-4 font-semibold text-white">{f.name}</td>
                  <td className="py-3 px-4">
                    <span className="badge badge-purple text-[10px]">{f.category?.replace('_', ' ')}</span>
                  </td>
                  <td className="py-3 px-4 text-emerald-400 font-bold">{Math.round(f.calories)} kcal</td>
                  <td className="py-3 px-4 text-blue-400">{f.protein_g}g</td>
                  <td className="py-3 px-4 text-amber-400">{f.carbs_g}g</td>
                  <td className="py-3 px-4 text-purple-400">{f.fat_g}g</td>
                  <td className="py-3 px-4 space-x-1">
                    {f.is_vegan && <span className="badge badge-green text-[9px]">Vegan</span>}
                    {f.is_vegetarian && !f.is_vegan && <span className="badge badge-blue text-[9px]">Veg</span>}
                    {f.is_gluten_free && <span className="badge badge-orange text-[9px]">GF</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
