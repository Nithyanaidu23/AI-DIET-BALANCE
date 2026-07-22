import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import {
  LayoutDashboard, Calendar, History, Search,
  Activity, User, Settings, LogOut, Zap,
  ShoppingCart, Droplets, Heart, Shield,
} from 'lucide-react'
import clsx from 'clsx'

const USER_NAV = [
  { to: '/dashboard', label: 'Dashboard',    icon: LayoutDashboard },
  { to: '/planner',   label: 'Meal Planner', icon: Calendar },
  { to: '/foods',     label: 'Food Search',  icon: Search },
  { to: '/history',   label: 'Meal History', icon: History },
  { to: '/grocery',   label: 'Grocery List', icon: ShoppingCart },
  { to: '/water',     label: 'Water Tracker',icon: Droplets },
  { to: '/bmi',       label: 'BMI & Macros', icon: Activity },
  { to: '/favorites', label: 'Favorites',    icon: Heart },
  { to: '/profile',   label: 'Profile',      icon: User },
  { to: '/settings',  label: 'Settings',     icon: Settings },
]

export default function Sidebar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <aside className="w-64 bg-surface-card border-r border-surface-border flex flex-col h-full shrink-0">
      {/* Logo */}
      <div className="p-5 border-b border-surface-border">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-brand-500 flex items-center justify-center shadow-glow-green">
              <Zap size={16} className="text-white" />
            </div>
            <div>
              <p className="font-bold font-display text-white text-sm leading-tight">AI Diet</p>
              <p className="text-xs text-brand-400">Planner</p>
            </div>
          </div>
          {user?.is_admin && (
            <NavLink to="/admin/dashboard" title="Go to Admin Console" className="p-1.5 rounded-lg bg-purple-500/20 text-purple-300 hover:bg-purple-500/30">
              <Shield size={14} />
            </NavLink>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-0.5 overflow-y-auto">
        <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-500 px-3 mb-2">User Workspace</p>
        {USER_NAV.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              clsx('nav-item', isActive && 'active')
            }
          >
            <Icon size={16} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* User + Logout */}
      <div className="p-4 border-t border-surface-border">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-8 h-8 rounded-full bg-brand-600/30 flex items-center justify-center text-brand-400 text-xs font-bold border border-brand-600/30">
            {user?.full_name?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || '?'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-medium text-slate-200 truncate">{user?.full_name || 'User'}</p>
            <p className="text-xs text-slate-500 truncate">{user?.email}</p>
          </div>
        </div>
        <button onClick={handleLogout} className="btn-ghost w-full justify-start text-xs text-red-400 hover:text-red-300 hover:bg-red-500/10">
          <LogOut size={13} />
          Sign out
        </button>
      </div>
    </aside>
  )
}
