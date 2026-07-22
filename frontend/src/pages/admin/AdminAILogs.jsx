import { useQuery } from '@tanstack/react-query'
import { adminService, exportService } from '../../services'
import LoadingSpinner from '../../components/LoadingSpinner'
import { Download, CheckCircle2, AlertCircle } from 'lucide-react'

export default function AdminAILogs() {
  const { data, isLoading } = useQuery({
    queryKey: ['admin-ai-logs'],
    queryFn: () => adminService.getAILogs().then((r) => r.data),
  })

  const logs = data?.ai_logs || []

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold font-display text-white">Gemini AI Request Logs</h1>
          <p className="text-xs text-slate-400">Audit prompt history, model performance, token estimates, and request statuses</p>
        </div>

        <button
          onClick={() => exportService.downloadFile('activity_logs.csv')}
          className="btn-secondary text-xs gap-1.5 w-full sm:w-auto"
        >
          <Download size={13} /> Export CSV
        </button>
      </div>

      {isLoading && <LoadingSpinner />}

      {!isLoading && (
        <div className="table-container">
          <table className="w-full text-left text-xs min-w-[650px]">
            <thead className="border-b border-slate-800 text-slate-400 uppercase tracking-wider bg-slate-900/50">
              <tr>
                <th className="py-3 px-4">User</th>
                <th className="py-3 px-4">Action</th>
                <th className="py-3 px-4">Prompt Description</th>
                <th className="py-3 px-4">IP Address</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50 text-slate-300">
              {logs.map((l) => (
                <tr key={l.id} className="hover:bg-slate-800/30">
                  <td className="py-3 px-4 font-semibold text-white">{l.user_email}</td>
                  <td className="py-3 px-4">
                    <span className="badge badge-purple text-[10px]">{l.action}</span>
                  </td>
                  <td className="py-3 px-4 text-slate-300 max-w-md truncate">{l.description}</td>
                  <td className="py-3 px-4 font-mono text-[11px] text-slate-500">{l.ip_address}</td>
                  <td className="py-3 px-4">
                    {l.status === 'SUCCESS' ? (
                      <span className="badge badge-green text-[10px] flex items-center gap-1 w-fit">
                        <CheckCircle2 size={10} /> Success
                      </span>
                    ) : (
                      <span className="badge badge-red text-[10px] flex items-center gap-1 w-fit">
                        <AlertCircle size={10} /> Failed
                      </span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-slate-500">{new Date(l.timestamp).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
