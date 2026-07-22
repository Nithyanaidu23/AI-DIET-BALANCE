import { Link } from 'react-router-dom'
import { Zap, Home } from 'lucide-react'

export default function NotFound() {
  return (
    <div className="min-h-screen bg-surface flex flex-col items-center justify-center text-center px-6">
      <div className="w-16 h-16 rounded-2xl bg-brand-500/20 flex items-center justify-center mb-6">
        <Zap size={28} className="text-brand-400" />
      </div>
      <h1 className="text-8xl font-bold font-display text-gradient mb-2">404</h1>
      <p className="text-2xl font-semibold text-white mb-2">Page not found</p>
      <p className="text-slate-400 text-sm mb-8 max-w-sm">
        The page you&apos;re looking for doesn&apos;t exist or has been moved.
      </p>
      <Link to="/dashboard" className="btn-primary gap-2">
        <Home size={15} /> Back to Dashboard
      </Link>
    </div>
  )
}
