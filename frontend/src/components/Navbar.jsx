import { useLocation } from 'react-router-dom'
import { useTheme } from '../context/ThemeContext'
import { Sun, Moon, Bell, Menu } from 'lucide-react'

const PAGE_TITLES = {
  '/dashboard': 'Dashboard',
  '/planner':   'Meal Planner',
  '/history':   'Meal History',
  '/foods':     'Food Search',
  '/bmi':       'BMI & Macros',
  '/profile':   'My Profile',
  '/settings':  'Settings',
}

export default function Navbar({ onMenuClick }) {
  const { pathname } = useLocation()
  const { toggleTheme, isDark } = useTheme()

  return (
    <header className="h-14 bg-surface-card border-b border-surface-border flex items-center px-4 sm:px-6 gap-3 shrink-0 sticky top-0 z-30">
      {/* Mobile Hamburger Toggle */}
      <button
        onClick={onMenuClick}
        className="btn-icon lg:hidden text-slate-300 hover:text-white"
        aria-label="Open navigation menu"
      >
        <Menu size={20} />
      </button>

      <h1 className="flex-1 text-sm sm:text-base font-semibold text-white truncate">
        {PAGE_TITLES[pathname] || 'AI Diet Planner'}
      </h1>

      <div className="flex items-center gap-1.5 sm:gap-2">
        {/* Notifications placeholder */}
        <button className="btn-icon relative" aria-label="Notifications">
          <Bell size={16} />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-brand-500 rounded-full" />
        </button>

        {/* Theme toggle */}
        <button onClick={toggleTheme} className="btn-icon" aria-label="Toggle theme">
          {isDark ? <Sun size={16} /> : <Moon size={16} />}
        </button>
      </div>
    </header>
  )
}
