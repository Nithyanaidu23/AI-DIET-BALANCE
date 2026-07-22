import { useLocation } from 'react-router-dom'
import { useTheme } from '../context/ThemeContext'
import { Sun, Moon, Bell } from 'lucide-react'

const PAGE_TITLES = {
  '/dashboard': 'Dashboard',
  '/planner':   'Meal Planner',
  '/history':   'Meal History',
  '/foods':     'Food Search',
  '/bmi':       'BMI & Macros',
  '/profile':   'My Profile',
  '/settings':  'Settings',
}

export default function Navbar() {
  const { pathname } = useLocation()
  const { toggleTheme, isDark } = useTheme()

  return (
    <header className="h-14 bg-surface-card border-b border-surface-border flex items-center px-6 gap-4 shrink-0">
      <h1 className="flex-1 text-base font-semibold text-white">
        {PAGE_TITLES[pathname] || 'AI Diet Planner'}
      </h1>

      <div className="flex items-center gap-2">
        {/* Notifications placeholder */}
        <button className="btn-icon relative" aria-label="Notifications">
          <Bell size={16} />
          <span className="absolute top-1 right-1 w-1.5 h-1.5 bg-brand-500 rounded-full" />
        </button>

        {/* Theme toggle */}
        <button onClick={toggleTheme} className="btn-icon" aria-label="Toggle theme">
          {isDark ? <Sun size={16} /> : <Moon size={16} />}
        </button>
      </div>
    </header>
  )
}
