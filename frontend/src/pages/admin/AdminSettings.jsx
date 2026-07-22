import { useQuery } from '@tanstack/react-query'
import { adminService, exportService } from '../../services'
import LoadingSpinner from '../../components/LoadingSpinner'
import { Cpu, HardDrive, Shield, RefreshCw } from 'lucide-react'
import toast from 'react-hot-toast'

export default function AdminSettings() {
  const { data: sys, isLoading } = useQuery({
    queryKey: ['admin-system-status'],
    queryFn: () => adminService.getSystemStatus().then((r) => r.data),
    refetchInterval: 15_000,
  })

  if (isLoading) return <LoadingSpinner label="Checking System Monitor…" />

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-xl sm:text-2xl font-bold font-display text-white">System Settings & Infrastructure</h1>
        <p className="text-xs text-slate-400">Configure platform backups, Gemini AI parameters, and server settings</p>
      </div>

      {/* System Health */}
      <div className="card space-y-4">
        <h2 className="text-sm font-semibold text-white flex items-center gap-2">
          <HardDrive size={16} className="text-purple-400" /> Infrastructure Monitoring
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
            <p className="text-slate-500">CPU Usage</p>
            <p className="text-base sm:text-lg font-bold text-white mt-1">{sys?.cpu_usage_percent}%</p>
          </div>
          <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
            <p className="text-slate-500">Memory RAM</p>
            <p className="text-base sm:text-lg font-bold text-purple-400 mt-1">{sys?.memory_percent}%</p>
            <p className="text-[10px] text-slate-500 truncate">{sys?.memory_used_mb} MB used</p>
          </div>
          <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
            <p className="text-slate-500">Database</p>
            <p className="text-base sm:text-lg font-bold text-emerald-400 mt-1 truncate">{sys?.database}</p>
          </div>
          <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
            <p className="text-slate-500">Gemini AI API</p>
            <p className="text-base sm:text-lg font-bold text-emerald-400 mt-1 truncate">{sys?.gemini_api}</p>
          </div>
        </div>
      </div>

      {/* AI Configuration */}
      <div className="card space-y-3">
        <h2 className="text-sm font-semibold text-white flex items-center gap-2">
          <Cpu size={16} className="text-emerald-400" /> Gemini Model Configuration
        </h2>
        <div className="space-y-2 text-xs">
          <div className="flex justify-between">
            <span className="text-slate-400">Model Name</span>
            <span className="text-slate-200 font-mono">gemini-1.5-flash</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">JSON Mode</span>
            <span className="text-emerald-400 font-semibold">Strict (application/json)</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Retry Strategy</span>
            <span className="text-slate-200">3 Attempts with Exponential Backoff</span>
          </div>
        </div>
      </div>

      {/* Automated Backups */}
      <div className="card space-y-4">
        <h2 className="text-sm font-semibold text-white flex items-center gap-2">
          <Shield size={16} className="text-blue-400" /> Automated Daily Backups
        </h2>
        <p className="text-xs text-slate-400">
          The background export engine automatically syncs DB state to <code className="text-purple-300">backend/exports/</code> in CSV and JSON formats on every transaction.
        </p>
        <button
          onClick={async () => {
            try {
              await exportService.syncExports()
              toast.success('System exports forced successfully!')
            } catch {
              toast.error('Sync failed')
            }
          }}
          className="btn-primary text-xs gap-2 w-full sm:w-auto"
        >
          <RefreshCw size={13} /> Trigger Emergency System Backup Now
        </button>
      </div>
    </div>
  )
}
