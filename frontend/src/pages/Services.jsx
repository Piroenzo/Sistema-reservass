import { useEffect, useState } from 'react'
import api from '../api/axios'
import useAuthStore from '../state/store'

const Services = () => {
  const businessId = useAuthStore((state) => state.user?.business_id)
  const [services, setServices] = useState([])
  const [form, setForm] = useState({ name: '', duration_minutes: 30, price: 0 })

  useEffect(() => {
    const load = async () => {
      if (!businessId) return
      const { data } = await api.get(`/businesses/${businessId}/services`)
      setServices(data)
    }
    load()
  }, [businessId])

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    const { data } = await api.post(`/businesses/${businessId}/services`, form)
    setServices((prev) => [...prev, data])
    setForm({ name: '', duration_minutes: 30, price: 0 })
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 md:col-span-1">
        <h2 className="text-xl font-semibold mb-3">Nuevo servicio</h2>
        <form className="space-y-3" onSubmit={handleSubmit}>
          <div>
            <label className="text-sm text-slate-300">Nombre</label>
            <input
              name="name"
              value={form.name}
              onChange={handleChange}
              className="mt-1 w-full rounded-lg bg-slate-800 border border-slate-700 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-rose-500"
            />
          </div>
          <div>
            <label className="text-sm text-slate-300">Duración (min)</label>
            <input
              name="duration_minutes"
              type="number"
              value={form.duration_minutes}
              onChange={handleChange}
              className="mt-1 w-full rounded-lg bg-slate-800 border border-slate-700 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-rose-500"
            />
          </div>
          <div>
            <label className="text-sm text-slate-300">Precio</label>
            <input
              name="price"
              type="number"
              value={form.price}
              onChange={handleChange}
              className="mt-1 w-full rounded-lg bg-slate-800 border border-slate-700 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-rose-500"
            />
          </div>
          <button className="w-full py-2 rounded-lg bg-rose-600 hover:bg-rose-700 font-semibold" type="submit">
            Guardar
          </button>
        </form>
      </div>
      <div className="md:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-4">
        <h2 className="text-xl font-semibold mb-3">Servicios</h2>
        <div className="divide-y divide-slate-800">
          {services.map((service) => (
            <div key={service.id} className="py-3 flex justify-between">
              <div>
                <p className="font-semibold">{service.name}</p>
                <p className="text-sm text-slate-400">
                  {service.duration_minutes} min · ${service.price}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Services
