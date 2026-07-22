import { useLocation, Link } from 'react-router-dom'
import { useTheme } from '../context/ThemeContext'
import { Sun, Moon, Bell, Shield, User } from 'lucide-react'

const PAGE_TITLES = {
  '/admin/dashboard':  'Creator Overview',
  '/admin/analytics':  'Platform Analytics',
  '/admin/users':      'User Management',
  '/admin/foods':      'Food Database CRUD',
  '/admin/meal-plans': 'Platform Meal Plans',
  '/admin/ai-logs':    'Gemini Request Audit',
  '/admin/reports':    'Data Export Center',
  '/admin/system':     'System Health Monitor',
  '/admin/settings':   'Admin Settings',
}

export default function AdminNavbar() {
  const { pathname } = useLocation()
  const { toggleTheme, isDark } = useTheme()

  return (
    <header className="h-14 bg-slate-900 border-b border-slate-800 flex items-center px-6 gap-4 shrink-0">
      <div className="flex items-center gap-2 flex-1">
        <Shield size={16} className="text-purple-400" />
        <h1 className="text-sm font-semibold text-white font-display">
          {PAGE_TITLES[pathname] || 'Admin Dashboard'}
        </h1>
      </div>

      <div className="flex items-center gap-3">
        <Link to="/dashboard" className="btn-secondary py-1 px-3 text-xs gap-1.5 border-purple-500/30 text-purple-300 hover:bg-purple-500/10">
          <User size={13} /> Switch to User App
        </Link>
        <button onClick={toggleTheme} className="btn-icon" aria-label="Toggle theme">
          {isDark ? <Sun size={15} /> : <Moon size={15} />}
        </button>
      </div>
    </header>
  )
}
