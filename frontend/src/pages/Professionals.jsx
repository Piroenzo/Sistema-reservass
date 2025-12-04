import { useEffect, useState } from 'react'
import api from '../api/axios'
import useAuthStore from '../state/store'

const Professionals = () => {
  const businessId = useAuthStore((state) => state.user?.business_id)
  const [professionals, setProfessionals] = useState([])
  const [name, setName] = useState('')

  useEffect(() => {
    const load = async () => {
      if (!businessId) return
      const { data } = await api.get(`/businesses/${businessId}/professionals`)
      setProfessionals(data)
    }
    load()
  }, [businessId])

  const handleSubmit = async (e) => {
    e.preventDefault()
    const { data } = await api.post(`/businesses/${businessId}/professionals`, { name })
    setProfessionals((prev) => [...prev, data])
    setName('')
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4">
        <h2 className="text-xl font-semibold mb-3">Nuevo profesional</h2>
        <form className="space-y-3" onSubmit={handleSubmit}>
          <div>
            <label className="text-sm text-slate-300">Nombre</label>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="mt-1 w-full rounded-lg bg-slate-800 border border-slate-700 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-rose-500"
            />
          </div>
          <button className="w-full py-2 rounded-lg bg-rose-600 hover:bg-rose-700 font-semibold" type="submit">
            Guardar
          </button>
        </form>
      </div>
      <div className="md:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-4">
        <h2 className="text-xl font-semibold mb-3">Equipo</h2>
        <div className="divide-y divide-slate-800">
          {professionals.map((pro) => (
            <div key={pro.id} className="py-3">
              <p className="font-semibold">{pro.name}</p>
              <p className="text-sm text-slate-400">ID Negocio: {pro.business_id}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Professionals
