import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import {
  LayoutDashboard, BarChart3, Users, Database,
  Calendar, Cpu, FileText, Activity, Settings, LogOut, ShieldCheck,
} from 'lucide-react'
import clsx from 'clsx'

const ADMIN_NAV = [
  { to: '/admin/dashboard',  label: 'Dashboard',    icon: LayoutDashboard },
  { to: '/admin/analytics',  label: 'Analytics',    icon: BarChart3 },
  { to: '/admin/users',      label: 'Users',        icon: Users },
  { to: '/admin/foods',      label: 'Food DB',      icon: Database },
  { to: '/admin/meal-plans', label: 'Meal Plans',   icon: Calendar },
  { to: '/admin/ai-logs',    label: 'AI Requests',  icon: Cpu },
  { to: '/admin/reports',    label: 'Reports',      icon: FileText },
  { to: '/admin/system',     label: 'System Monitor',icon: Activity },
  { to: '/admin/settings',   label: 'Settings',     icon: Settings },
]

export default function AdminSidebar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-full shrink-0">
      {/* Brand */}
      <div className="p-5 border-b border-slate-800">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-purple-500/20">
            <ShieldCheck size={18} className="text-white" />
          </div>
          <div>
            <p className="font-bold font-display text-white text-sm leading-tight">Admin Console</p>
            <span className="badge badge-purple text-[10px] mt-0.5">Creator SaaS</span>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 p-3 space-y-0.5 overflow-y-auto">
        <p className="text-[10px] font-semibold uppercase tracking-wider text-slate-500 px-3 mb-2">Platform Management</p>
        {ADMIN_NAV.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              clsx(
                'flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 cursor-pointer',
                isActive
                  ? 'bg-purple-600/20 text-purple-300 border border-purple-500/30 shadow-glow-purple'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/60'
              )
            }
          >
            <Icon size={16} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* User profile */}
      <div className="p-4 border-t border-slate-800 bg-slate-950/40">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-8 h-8 rounded-full bg-purple-600/30 flex items-center justify-center text-purple-300 text-xs font-bold border border-purple-500/40">
            {user?.full_name?.[0]?.toUpperCase() || 'A'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-medium text-slate-200 truncate">{user?.full_name || 'Admin User'}</p>
            <p className="text-xs text-purple-400 font-mono">Role: {user?.role || 'Admin'}</p>
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
