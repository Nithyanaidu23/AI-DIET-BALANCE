import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Zap, Mail, Lock, User, Eye, EyeOff } from 'lucide-react'
import { useState } from 'react'
import toast from 'react-hot-toast'

const schema = z.object({
  first_name: z.string().min(1, 'First name is required'),
  last_name:  z.string().optional(),
  email:      z.string().email('Enter a valid email'),
  password:   z.string().min(8, 'Minimum 8 characters'),
  password2:  z.string(),
}).refine((d) => d.password === d.password2, {
  message: 'Passwords do not match',
  path: ['password2'],
})

export default function Register() {
  const { register: registerUser } = useAuth()
  const navigate = useNavigate()
  const [showPw, setShowPw] = useState(false)

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data) => {
    try {
      await registerUser(data)
      toast.success('Account created! Welcome to AI Diet Planner.')
      navigate('/dashboard')
    } catch (err) {
      const msgs = err.response?.data
      if (msgs && typeof msgs === 'object') {
        Object.values(msgs).flat().forEach((m) => toast.error(m))
      } else {
        toast.error('Registration failed. Try again.')
      }
    }
  }

  return (
    <div className="min-h-screen bg-surface flex items-center justify-center p-4 sm:p-6 lg:p-12 overflow-x-hidden">
      <div className="w-full max-w-lg">
        <div className="flex items-center gap-2 mb-8">
          <div className="w-8 h-8 rounded-lg bg-brand-500 flex items-center justify-center shadow-glow-green">
            <Zap size={16} className="text-white" />
          </div>
          <span className="font-bold text-white font-display">AI Diet Planner</span>
        </div>

        <div className="card p-6 sm:p-8 animate-in">
          <h1 className="text-xl sm:text-2xl font-bold font-display text-white mb-1">Create your account</h1>
          <p className="text-xs sm:text-sm text-slate-400 mb-6 sm:mb-8">Start your personalised nutrition journey</p>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
              <div>
                <label className="input-label">First name</label>
                <div className="relative">
                  <User size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                  <input {...register('first_name')} className="input pl-9" placeholder="Ravi" id="first_name" />
                </div>
                {errors.first_name && <p className="input-error">{errors.first_name.message}</p>}
              </div>
              <div>
                <label className="input-label">Last name</label>
                <input {...register('last_name')} className="input" placeholder="Kumar" id="last_name" />
              </div>
            </div>

            <div>
              <label className="input-label">Email address</label>
              <div className="relative">
                <Mail size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                <input {...register('email')} type="email" className="input pl-9" placeholder="you@example.com" id="email" autoComplete="email" />
              </div>
              {errors.email && <p className="input-error">{errors.email.message}</p>}
            </div>

            <div>
              <label className="input-label">Password</label>
              <div className="relative">
                <Lock size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                <input
                  {...register('password')}
                  type={showPw ? 'text' : 'password'}
                  className="input pl-9 pr-10"
                  placeholder="At least 8 characters"
                  id="password"
                />
                <button type="button" onClick={() => setShowPw((v) => !v)} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300">
                  {showPw ? <EyeOff size={14} /> : <Eye size={14} />}
                </button>
              </div>
              {errors.password && <p className="input-error">{errors.password.message}</p>}
            </div>

            <div>
              <label className="input-label">Confirm password</label>
              <input
                {...register('password2')}
                type={showPw ? 'text' : 'password'}
                className="input"
                placeholder="Repeat password"
                id="password2"
              />
              {errors.password2 && <p className="input-error">{errors.password2.message}</p>}
            </div>

            <button type="submit" className="btn-primary w-full py-3" disabled={isSubmitting}>
              {isSubmitting ? 'Creating account…' : 'Create account'}
            </button>
          </form>

          <div className="divider" />

          <p className="text-center text-xs sm:text-sm text-slate-400">
            Already have an account?{' '}
            <Link to="/login" className="text-brand-400 hover:text-brand-300 font-medium">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
