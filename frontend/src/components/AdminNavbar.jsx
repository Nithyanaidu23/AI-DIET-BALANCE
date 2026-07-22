import { useLocation, Link } from 'react-router-dom'
import { useTheme } from '../context/ThemeContext'
import { Sun, Moon, Shield, User, Menu } from 'lucide-react'

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

export default function AdminNavbar({ onMenuClick }) {
  const { pathname } = useLocation()
  const { toggleTheme, isDark } = useTheme()

  return (
    <header className="h-14 bg-slate-900 border-b border-slate-800 flex items-center px-4 sm:px-6 gap-3 shrink-0 sticky top-0 z-30">
      <button
        onClick={onMenuClick}
        className="btn-icon lg:hidden text-slate-300 hover:text-white"
        aria-label="Open admin navigation menu"
      >
        <Menu size={20} />
      </button>

      <div className="flex items-center gap-2 flex-1 min-w-0">
        <Shield size={16} className="text-purple-400 shrink-0" />
        <h1 className="text-xs sm:text-sm font-semibold text-white font-display truncate">
          {PAGE_TITLES[pathname] || 'Admin Dashboard'}
        </h1>
      </div>

      <div className="flex items-center gap-2 sm:gap-3">
        <Link to="/dashboard" className="btn-secondary py-1 px-2.5 sm:px-3 text-xs gap-1.5 border-purple-500/30 text-purple-300 hover:bg-purple-500/10">
          <User size={13} /> <span className="hidden sm:inline">Switch to</span> User App
        </Link>
        <button onClick={toggleTheme} className="btn-icon" aria-label="Toggle theme">
          {isDark ? <Sun size={15} /> : <Moon size={15} />}
        </button>
      </div>
    </header>
  )
}
