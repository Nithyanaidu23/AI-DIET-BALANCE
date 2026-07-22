import { useQuery } from '@tanstack/react-query'
import { exportService } from '../../services'
import LoadingSpinner from '../../components/LoadingSpinner'
import { Download, FileText, FileArchive, RefreshCw } from 'lucide-react'
import toast from 'react-hot-toast'

export default function AdminReports() {
  const { data, isLoading, refetch } = useQuery({
    queryKey: ['export-files-list'],
    queryFn: () => exportService.getExports().then((r) => r.data),
  })

  const files = data?.files || []

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold font-display text-white">Data Export & Backup Center</h1>
          <p className="text-xs text-slate-400">Download system data in CSV, JSON, or bundled ZIP archives</p>
        </div>

        <div className="flex gap-3">
          <button
            onClick={() => exportService.downloadZip()}
            className="btn-primary text-xs gap-2"
          >
            <FileArchive size={14} /> Download ZIP Archive
          </button>

          <button
            onClick={async () => {
              try {
                await exportService.syncExports()
                refetch()
                toast.success('Exports resynchronized successfully!')
              } catch {
                toast.error('Sync failed')
              }
            }}
            className="btn-secondary text-xs gap-1.5"
          >
            <RefreshCw size={13} /> Re-sync All Files
          </button>
        </div>
      </div>

      {isLoading && <LoadingSpinner />}

      {!isLoading && (
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {files.map((f) => (
            <div key={f.name} className="card hover-lift flex flex-col justify-between p-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className={`badge text-[10px] ${f.type === 'CSV' ? 'badge-blue' : 'badge-purple'}`}>
                    {f.type}
                  </span>
                  <FileText size={16} className="text-slate-500" />
                </div>
                <p className="font-semibold text-white text-xs truncate">{f.name}</p>
                <p className="text-[11px] text-slate-500 mt-1">{(f.size_bytes / 1024).toFixed(1)} KB</p>
              </div>

              <button
                onClick={() => exportService.downloadFile(f.name)}
                className="btn-secondary text-xs w-full mt-4 justify-center gap-1.5"
              >
                <Download size={12} /> Download
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
