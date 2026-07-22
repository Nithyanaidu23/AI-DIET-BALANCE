import clsx from 'clsx'

export default function LoadingSpinner({ fullScreen = false, size = 'md', label = 'Loading…' }) {
  const sizes = { sm: 'w-4 h-4', md: 'w-8 h-8', lg: 'w-12 h-12' }

  const spinner = (
    <div className="flex flex-col items-center gap-3">
      <div className={clsx('rounded-full border-2 border-brand-600/30 border-t-brand-500 animate-spin', sizes[size])} />
      {label && <p className="text-sm text-slate-400">{label}</p>}
    </div>
  )

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-surface flex items-center justify-center z-50">
        {spinner}
      </div>
    )
  }

  return <div className="flex items-center justify-center py-12">{spinner}</div>
}
