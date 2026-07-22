import { useTheme } from '../context/ThemeContext'
import { useAuth } from '../context/AuthContext'
import { Moon, Sun, LogOut } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { authService, exportService } from '../services'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import toast from 'react-hot-toast'

const pwSchema = z.object({
  old_password:  z.string().min(1),
  new_password:  z.string().min(8, 'Minimum 8 characters'),
  new_password2: z.string(),
}).refine((d) => d.new_password === d.new_password2, { message: 'Passwords do not match', path: ['new_password2'] })

export default function Settings() {
  const { isDark, toggleTheme } = useTheme()
  const { logout, user } = useAuth()
  const navigate = useNavigate()

  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm({
    resolver: zodResolver(pwSchema),
  })

  const changePw = useMutation({
    mutationFn: (d) => authService.changePassword(d),
    onSuccess: () => { toast.success('Password changed!'); reset() },
    onError: (e) => toast.error(e.response?.data?.old_password || 'Failed to change password.'),
  })

  const handleLogout = () => { logout(); navigate('/login') }

  return (
    <div className="page-container max-w-2xl">
      <div className="page-header">
        <h1 className="page-title">Settings</h1>
        <p className="page-subtitle">Manage your account preferences</p>
      </div>

      <div className="space-y-6">
        {/* Theme */}
        <div className="card">
          <h2 className="font-semibold text-white text-sm mb-4">Appearance</h2>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-200">Dark Mode</p>
              <p className="text-xs text-slate-500">Toggle between light and dark theme</p>
            </div>
            <button
              onClick={toggleTheme}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none ${isDark ? 'bg-brand-600' : 'bg-slate-600'}`}
              aria-label="Toggle dark mode"
              id="theme-toggle"
            >
              <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${isDark ? 'translate-x-6' : 'translate-x-1'}`} />
            </button>
          </div>
        </div>

        {/* Account info */}
        <div className="card">
          <h2 className="font-semibold text-white text-sm mb-4">Account</h2>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-slate-400">Email</span>
              <span className="text-slate-200">{user?.email}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Name</span>
              <span className="text-slate-200">{user?.full_name || '—'}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Role</span>
              <span className="text-slate-200">{user?.is_staff ? 'Admin' : 'Member'}</span>
            </div>
          </div>
        </div>

        {/* Change password */}
        <div className="card">
          <h2 className="font-semibold text-white text-sm mb-4">Change Password</h2>
          <form onSubmit={handleSubmit((d) => changePw.mutate(d))} className="space-y-4">
            {[
              { name: 'old_password',  label: 'Current Password',  auto: 'current-password' },
              { name: 'new_password',  label: 'New Password',       auto: 'new-password'     },
              { name: 'new_password2', label: 'Confirm New Password',auto: 'new-password'    },
            ].map(({ name, label, auto }) => (
              <div key={name}>
                <label className="input-label text-xs">{label}</label>
                <input {...register(name)} type="password" className="input text-sm py-2" autoComplete={auto} />
                {errors[name] && <p className="input-error">{errors[name].message}</p>}
              </div>
            ))}
            <button type="submit" className="btn-primary text-sm" disabled={isSubmitting}>
              {isSubmitting ? 'Changing…' : 'Update Password'}
            </button>
          </form>
        </div>

        {/* Data Exports */}
        <div className="card">
          <h2 className="font-semibold text-white text-sm mb-1">Data Exports & Audit Backup</h2>
          <p className="text-xs text-slate-400 mb-4">Export all database records and audit history to CSV and JSON formats.</p>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => exportService.downloadZip()}
              className="btn-primary text-xs gap-2"
            >
              Download Full Backup (.zip)
            </button>
            <button
              onClick={async () => {
                try {
                  await exportService.syncExports()
                  toast.success('Exports resynchronized successfully!')
                } catch {
                  toast.error('Failed to sync exports.')
                }
              }}
              className="btn-secondary text-xs"
            >
              Re-sync CSV / JSON Files
            </button>
          </div>
        </div>

        {/* Danger zone */}
        <div className="card border-red-900/30">
          <h2 className="font-semibold text-red-400 text-sm mb-4">Danger Zone</h2>
          <button onClick={handleLogout} className="btn-danger text-sm gap-2">
            <LogOut size={14} /> Sign Out of All Devices
          </button>
        </div>
      </div>
    </div>
  )
}
