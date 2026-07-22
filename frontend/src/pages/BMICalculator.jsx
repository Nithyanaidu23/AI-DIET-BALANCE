import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { useForm } from 'react-hook-form'
import { healthService } from '../services'
import NutritionChart from '../components/NutritionChart'
import toast from 'react-hot-toast'
import { Activity, Scale, Droplets, Target } from 'lucide-react'

function ResultCard({ label, value, sub, color = 'brand' }) {
  const colors = {
    brand:  'from-brand-600/20 to-brand-700/10 border-brand-600/20  text-brand-400',
    blue:   'from-blue-600/20  to-blue-700/10  border-blue-600/20   text-blue-400',
    purple: 'from-purple-600/20 to-purple-700/10 border-purple-600/20 text-purple-400',
    amber:  'from-amber-600/20 to-amber-700/10 border-amber-600/20  text-amber-400',
    teal:   'from-teal-600/20  to-teal-700/10  border-teal-600/20   text-teal-400',
  }
  return (
    <div className={`rounded-xl border bg-gradient-to-br p-4 ${colors[color]}`}>
      <p className="text-xs font-medium opacity-70 mb-1">{label}</p>
      <p className="text-2xl font-bold text-white">{value}</p>
      {sub && <p className="text-xs mt-0.5 opacity-60">{sub}</p>}
    </div>
  )
}

export default function BMICalculator() {
  const [result, setResult] = useState(null)
  const { register, handleSubmit } = useForm({
    defaultValues: { age: 25, gender: 'male', weight_kg: 70, height_cm: 170, activity_level: 'moderate', goal: 'lose_fat', save_record: true },
  })

  const calc = useMutation({
    mutationFn: (d) => healthService.calculateBMI(d).then((r) => r.data),
    onSuccess: (data) => { setResult(data); toast.success('BMI calculated!') },
    onError: () => toast.error('Calculation failed.'),
  })

  const bmiColor = result ? (
    result.bmi < 18.5 ? 'text-blue-400' :
    result.bmi < 25   ? 'text-brand-400' :
    result.bmi < 30   ? 'text-amber-400' : 'text-red-400'
  ) : 'text-white'

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">BMI & Calorie Calculator</h1>
        <p className="page-subtitle">Using Mifflin-St Jeor BMR and TDEE formulas — no AI guessing</p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Form */}
        <form onSubmit={handleSubmit((d) => calc.mutate(d))} className="card space-y-4">
          <h2 className="font-semibold text-white text-sm">Enter Your Measurements</h2>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="input-label text-xs">Age</label>
              <input {...register('age', { valueAsNumber: true })} type="number" className="input py-2" placeholder="25" id="bmi-age" />
            </div>
            <div>
              <label className="input-label text-xs">Gender</label>
              <select {...register('gender')} className="select py-2" id="bmi-gender">
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label className="input-label text-xs">Weight (kg)</label>
              <input {...register('weight_kg', { valueAsNumber: true })} type="number" step="0.1" className="input py-2" placeholder="70" id="bmi-weight" />
            </div>
            <div>
              <label className="input-label text-xs">Height (cm)</label>
              <input {...register('height_cm', { valueAsNumber: true })} type="number" className="input py-2" placeholder="170" id="bmi-height" />
            </div>
          </div>

          <div>
            <label className="input-label text-xs">Activity Level</label>
            <select {...register('activity_level')} className="select py-2" id="bmi-activity">
              <option value="sedentary">Sedentary</option>
              <option value="light">Lightly Active</option>
              <option value="moderate">Moderately Active</option>
              <option value="very">Very Active</option>
              <option value="extra">Extra Active</option>
            </select>
          </div>

          <div>
            <label className="input-label text-xs">Fitness Goal</label>
            <select {...register('goal')} className="select py-2" id="bmi-goal">
              <option value="lose_fat">Lose Fat</option>
              <option value="build_muscle">Build Muscle</option>
              <option value="maintain">Maintain</option>
              <option value="improve_health">Improve Health</option>
              <option value="increase_endurance">Endurance</option>
            </select>
          </div>

          <label className="flex items-center gap-2 text-sm text-slate-300 cursor-pointer">
            <input {...register('save_record')} type="checkbox" defaultChecked className="accent-brand-500 w-4 h-4 rounded" />
            Save this record for progress tracking
          </label>

          <button type="submit" className="btn-primary w-full" disabled={calc.isPending}>
            {calc.isPending ? 'Calculating…' : <span className="flex items-center justify-center gap-2"><Activity size={15} /> Calculate</span>}
          </button>
        </form>

        {/* Results */}
        {result && (
          <div className="space-y-4 animate-in">
            <div className="card text-center">
              <p className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-1">Your BMI</p>
              <p className={`text-6xl font-bold font-display ${bmiColor}`}>{result.bmi}</p>
              <p className={`text-sm font-medium mt-1 ${bmiColor}`}>{result.bmi_category}</p>

              {/* Simple BMI bar */}
              <div className="mt-4 relative h-3 rounded-full bg-gradient-to-r from-blue-400 via-brand-500 via-amber-400 to-red-500 overflow-hidden">
                <div
                  className="absolute top-0 h-full w-0.5 bg-white shadow-lg"
                  style={{ left: `${Math.min(95, Math.max(5, ((result.bmi - 15) / 25) * 100))}%` }}
                />
              </div>
              <div className="flex justify-between text-[10px] text-slate-500 mt-1">
                <span>Under</span><span>Normal</span><span>Over</span><span>Obese</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <ResultCard label="BMR" value={`${result.bmr}`} sub="kcal/day at rest" color="blue" />
              <ResultCard label="TDEE" value={`${result.tdee}`} sub="kcal/day with activity" color="purple" />
              <ResultCard label="Goal Calories" value={`${result.goal_calories}`} sub="kcal/day" color="brand" />
              <ResultCard label="Water Intake" value={`${Math.round(result.water_intake_ml / 100) / 10}L`} sub="per day" color="teal" />
              <ResultCard label="Body Fat Est." value={`${result.body_fat_percent}%`} sub="estimation only" color="amber" />
              <ResultCard label="Ideal Weight" value={`${result.ideal_weight_kg} kg`} sub="Devine formula" color="brand" />
            </div>

            <div className="card">
              <h3 className="text-xs font-semibold text-white mb-3 uppercase tracking-wider">Recommended Macros</h3>
              <NutritionChart protein={result.protein_g} carbs={result.carbs_g} fat={result.fat_g} size={180} />
            </div>
          </div>
        )}

        {!result && !calc.isPending && (
          <div className="card flex flex-col items-center justify-center py-20 text-slate-500 text-center">
            <Scale size={40} className="mb-4 opacity-30" />
            <p className="text-sm">Enter your measurements to see your BMI, BMR, TDEE, and macro targets</p>
          </div>
        )}
      </div>
    </div>
  )
}
