import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { adminService } from '../../services'
import LoadingSpinner from '../../components/LoadingSpinner'
import { Search, Shield, UserCheck, UserX, Trash2 } from 'lucide-react'
import toast from 'react-hot-toast'

export default function AdminUsers() {
  const [search, setSearch] = useState('')
  const [roleFilter, setRoleFilter] = useState('')
  const qc = useQueryClient()

  const { data: users, isLoading } = useQuery({
    queryKey: ['admin-users', search, roleFilter],
    queryFn: () => adminService.getUsers({ search: search || undefined, role: roleFilter || undefined }).then((r) => r.data),
  })

  const updateUser = useMutation({
    mutationFn: (payload) => adminService.updateUser(payload),
    onSuccess: () => {
      qc.invalidateQueries(['admin-users'])
      toast.success('User updated successfully')
    },
    onError: () => toast.error('Failed to update user'),
  })

  const list = users?.results || users || []

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold font-display text-white">User Management</h1>
          <p className="text-xs text-slate-400">View, update roles, suspend or activate registered accounts</p>
        </div>
      </div>

      {/* Filters */}
      <div className="card flex flex-wrap gap-4">
        <div className="flex-1 min-w-48 relative">
          <Search size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input pl-10 py-2 text-sm"
            placeholder="Search by name or email…"
          />
        </div>
        <select
          value={roleFilter}
          onChange={(e) => setRoleFilter(e.target.value)}
          className="select text-sm py-2 w-44"
        >
          <option value="">All Roles</option>
          <option value="admin">Admin</option>
          <option value="user">User</option>
        </select>
      </div>

      {isLoading && <LoadingSpinner />}

      {!isLoading && (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="border-b border-slate-800 text-slate-400 uppercase tracking-wider bg-slate-900/50">
                <tr>
                  <th className="py-3 px-4">User</th>
                  <th className="py-3 px-4">Role</th>
                  <th className="py-3 px-4">Joined</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50 text-slate-300">
                {list.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-800/30">
                    <td className="py-3 px-4">
                      <p className="font-semibold text-white">{u.full_name || 'No Name'}</p>
                      <p className="text-slate-500 text-[11px]">{u.email}</p>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`badge text-[10px] ${u.role === 'admin' ? 'badge-purple' : 'badge-blue'}`}>
                        {u.role?.toUpperCase() || 'USER'}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-400">
                      {new Date(u.date_joined).toLocaleDateString()}
                    </td>
                    <td className="py-3 px-4">
                      {u.is_active ? (
                        <span className="badge badge-green text-[10px]">Active</span>
                      ) : (
                        <span className="badge badge-red text-[10px]">Suspended</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-right space-x-2">
                      {u.role !== 'admin' ? (
                        <button
                          onClick={() => updateUser.mutate({ user_id: u.id, role: 'admin' })}
                          className="btn-secondary py-1 px-2 text-[11px] gap-1"
                        >
                          <Shield size={11} /> Make Admin
                        </button>
                      ) : (
                        <button
                          onClick={() => updateUser.mutate({ user_id: u.id, role: 'user' })}
                          className="btn-secondary py-1 px-2 text-[11px]"
                        >
                          Demote to User
                        </button>
                      )}

                      <button
                        onClick={() => updateUser.mutate({ user_id: u.id, is_active: !u.is_active })}
                        className={`btn-ghost py-1 px-2 text-[11px] ${u.is_active ? 'text-red-400 hover:bg-red-500/10' : 'text-emerald-400'}`}
                      >
                        {u.is_active ? 'Suspend' : 'Activate'}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
