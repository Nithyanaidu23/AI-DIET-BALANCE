import { useForm } from 'react-hook-form'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { profileService } from '../services'
import { useAuth } from '../context/AuthContext'
import LoadingSpinner from '../components/LoadingSpinner'
import toast from 'react-hot-toast'
import { Save } from 'lucide-react'

const FIELDS = [
  { key: 'age',               label: 'Age',                  type: 'number',  placeholder: '25' },
  { key: 'height_cm',         label: 'Height (cm)',          type: 'number',  placeholder: '170' },
  { key: 'weight_kg',         label: 'Weight (kg)',          type: 'number',  placeholder: '70' },
  { key: 'country',           label: 'Country',              type: 'text',    placeholder: 'India' },
  { key: 'cuisine_preference',label: 'Cuisine Preference',   type: 'text',    placeholder: 'Indian, Mediterranean' },
  { key: 'budget_per_day_usd',label: 'Daily Budget (USD)',   type: 'number',  placeholder: '15' },
  { key: 'workout_time',      label: 'Workout Time',         type: 'text',    placeholder: 'Morning' },
  { key: 'allergies',         label: 'Allergies',            type: 'text',    placeholder: 'peanuts, shellfish' },
  { key: 'medical_conditions',label: 'Medical Conditions',   type: 'text',    placeholder: 'diabetes, hypertension' },
]

export default function Profile() {
  const { user } = useAuth()
  const qc = useQueryClient()

  const { data: profile, isLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: () => profileService.get().then((r) => r.data),
  })

  const { register, handleSubmit, formState: { isSubmitting } } = useForm({
    values: profile || {},
  })

  const update = useMutation({
    mutationFn: (data) => profileService.update(data),
    onSuccess: () => { qc.invalidateQueries(['profile']); toast.success('Profile updated!') },
    onError: () => toast.error('Update failed.'),
  })

  if (isLoading) return <LoadingSpinner />

  return (
    <div className="page-container space-y-6">
      <div className="page-header">
        <h1 className="page-title">My Profile</h1>
        <p className="page-subtitle">Update your health info for more accurate AI meal plans</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Avatar card */}
        <div className="card text-center py-8 lg:col-span-1">
          <div className="w-20 h-20 rounded-full bg-brand-600/30 border-2 border-brand-600/40 flex items-center justify-center text-3xl font-bold text-brand-400 mx-auto mb-4">
            {user?.full_name?.[0]?.toUpperCase() || '?'}
          </div>
          <h2 className="font-bold text-white text-base sm:text-lg">{user?.full_name || '—'}</h2>
          <p className="text-xs text-slate-400 mt-0.5 truncate">{user?.email}</p>
          {profile?.is_complete ? (
            <span className="badge badge-green mt-3 mx-auto">Profile Complete</span>
          ) : (
            <span className="badge badge-orange mt-3 mx-auto">Incomplete</span>
          )}

          {profile && (
            <div className="mt-6 space-y-2 text-xs text-left">
              {[
                { label: 'Goal',     value: profile.fitness_goal?.replace('_', ' ') },
                { label: 'Activity', value: profile.activity_level },
                { label: 'Diet',     value: profile.food_preference },
              ].map(({ label, value }) => value && (
                <div key={label} className="flex justify-between">
                  <span className="text-slate-500">{label}</span>
                  <span className="text-slate-300 capitalize">{value}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit((d) => update.mutate(d))} className="card lg:col-span-2 space-y-5">
          <h2 className="font-semibold text-white text-sm">Physical & Lifestyle Details</h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
            <div>
              <label className="input-label text-xs">Gender</label>
              <select {...register('gender')} className="select text-sm py-2" id="profile-gender">
                <option value="">Select…</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
                <option value="prefer_not_to_say">Prefer not to say</option>
              </select>
            </div>
            <div>
              <label className="input-label text-xs">Fitness Goal</label>
              <select {...register('fitness_goal')} className="select text-sm py-2" id="profile-goal">
                <option value="lose_fat">Lose Fat</option>
                <option value="build_muscle">Build Muscle</option>
                <option value="maintain">Maintain</option>
                <option value="improve_health">Improve Health</option>
                <option value="increase_endurance">Endurance</option>
              </select>
            </div>
            <div>
              <label className="input-label text-xs">Activity Level</label>
              <select {...register('activity_level')} className="select text-sm py-2" id="profile-activity">
                <option value="sedentary">Sedentary</option>
                <option value="light">Lightly Active</option>
                <option value="moderate">Moderately Active</option>
                <option value="very">Very Active</option>
                <option value="extra">Extra Active</option>
              </select>
            </div>
            <div>
              <label className="input-label text-xs">Food Preference</label>
              <select {...register('food_preference')} className="select text-sm py-2" id="profile-foodpref">
                <option value="none">No Preference</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="vegan">Vegan</option>
                <option value="pescatarian">Pescatarian</option>
                <option value="keto">Keto</option>
                <option value="gluten_free">Gluten-Free</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
            {FIELDS.map(({ key, label, type, placeholder }) => (
              <div key={key}>
                <label className="input-label text-xs" htmlFor={`profile-${key}`}>{label}</label>
                <input
                  {...register(key)}
                  id={`profile-${key}`}
                  type={type}
                  step={type === 'number' ? '0.1' : undefined}
                  className="input text-sm py-2"
                  placeholder={placeholder}
                />
              </div>
            ))}
          </div>

          <button type="submit" className="btn-primary gap-2 w-full sm:w-auto" disabled={isSubmitting}>
            <Save size={14} /> {isSubmitting ? 'Saving…' : 'Save Profile'}
          </button>
        </form>
      </div>
    </div>
  )
}
