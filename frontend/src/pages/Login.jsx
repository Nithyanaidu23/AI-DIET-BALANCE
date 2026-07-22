import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Zap, Mail, Lock, Eye, EyeOff } from 'lucide-react'
import { useState } from 'react'
import toast from 'react-hot-toast'

const schema = z.object({
  email:    z.string().email('Enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [showPw, setShowPw] = useState(false)

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data) => {
    try {
      await login(data.email, data.password)
      toast.success('Welcome back!')
      navigate('/dashboard')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Invalid credentials.')
    }
  }

  return (
    <div className="min-h-screen bg-surface flex overflow-x-hidden">
      {/* Left panel */}
      <div className="hidden lg:flex flex-1 bg-gradient-to-br from-surface via-brand-950/30 to-surface items-center justify-center p-12">
        <div className="max-w-sm">
          <div className="flex items-center gap-2.5 mb-10">
            <div className="w-10 h-10 rounded-xl bg-brand-500 flex items-center justify-center shadow-glow-green">
              <Zap size={20} className="text-white" />
            </div>
            <span className="text-xl font-bold font-display text-white">AI Diet Planner</span>
          </div>
          <h2 className="text-4xl font-bold font-display text-white mb-4 leading-tight">
            Your journey to <span className="text-gradient">better health</span> starts here.
          </h2>
          <p className="text-slate-400 text-sm leading-relaxed">
            Sign in to access your personalised AI meal plans, macro tracker, and nutrition insights.
          </p>
        </div>
      </div>

      {/* Right panel — form */}
      <div className="flex-1 flex items-center justify-center p-4 sm:p-6 lg:p-12">
        <div className="w-full max-w-md">
          {/* Mobile logo */}
          <div className="flex items-center gap-2 mb-8 lg:hidden">
            <div className="w-8 h-8 rounded-lg bg-brand-500 flex items-center justify-center">
              <Zap size={16} className="text-white" />
            </div>
            <span className="font-bold text-white font-display">AI Diet Planner</span>
          </div>

          <div className="card p-6 sm:p-8 animate-in">
            <h1 className="text-xl sm:text-2xl font-bold font-display text-white mb-1">Welcome back</h1>
            <p className="text-xs sm:text-sm text-slate-400 mb-6 sm:mb-8">Sign in to your account</p>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 sm:space-y-5">
              <div>
                <label className="input-label">Email address</label>
                <div className="relative">
                  <Mail size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                  <input
                    {...register('email')}
                    type="email"
                    className="input pl-10"
                    placeholder="you@example.com"
                    id="email"
                    autoComplete="email"
                  />
                </div>
                {errors.email && <p className="input-error">{errors.email.message}</p>}
              </div>

              <div>
                <label className="input-label">Password</label>
                <div className="relative">
                  <Lock size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                  <input
                    {...register('password')}
                    type={showPw ? 'text' : 'password'}
                    className="input pl-10 pr-10"
                    placeholder="••••••••"
                    id="password"
                    autoComplete="current-password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPw((v) => !v)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300"
                  >
                    {showPw ? <EyeOff size={15} /> : <Eye size={15} />}
                  </button>
                </div>
                {errors.password && <p className="input-error">{errors.password.message}</p>}
              </div>

              <button type="submit" className="btn-primary w-full py-3" disabled={isSubmitting}>
                {isSubmitting ? 'Signing in…' : 'Sign in'}
              </button>
            </form>

            <div className="divider" />

            <p className="text-center text-xs sm:text-sm text-slate-400">
              Don&apos;t have an account?{' '}
              <Link to="/register" className="text-brand-400 hover:text-brand-300 font-medium">
                Create one free
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
