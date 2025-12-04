import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import api from '../api/axios'

const StatCard = ({ title, value, accent = 'rose' }) => (
  <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4">
    <p className="text-sm text-slate-400">{title}</p>
    <p className="text-3xl font-bold text-white mt-1">{value}</p>
    <span className={`text-xs uppercase tracking-wide text-${accent}-400`}>Últimos 30 días</span>
  </div>
)

const Dashboard = () => {
  const [stats, setStats] = useState({ total: 0, cancelled: 0, no_show: 0, top_services: [] })

  useEffect(() => {
    const loadStats = async () => {
      const { data } = await api.get('/stats')
      setStats(data)
    }
    loadStats()
  }, [])

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard title="Turnos" value={stats.total} />
        <StatCard title="Cancelados" value={stats.cancelled} accent="amber" />
        <StatCard title="Ausencias" value={stats.no_show} accent="cyan" />
      </div>
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4">
        <h3 className="text-lg font-semibold mb-4">Top servicios</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={stats.top_services}>
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" fill="#f43f5e" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
