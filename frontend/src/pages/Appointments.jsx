import { useEffect, useState } from 'react'
import api from '../api/axios'

const Appointments = () => {
  const [appointments, setAppointments] = useState([])

  useEffect(() => {
    const load = async () => {
      const { data } = await api.get('/appointments')
      setAppointments(data)
    }
    load()
  }, [])

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4">
      <h2 className="text-xl font-semibold mb-4">Turnos</h2>
      <div className="divide-y divide-slate-800">
        {appointments.map((appt) => (
          <div key={appt.id} className="py-3 flex justify-between items-center">
            <div>
              <p className="font-semibold">Servicio #{appt.service_id}</p>
              <p className="text-sm text-slate-400">
                Profesional {appt.professional_id} · {new Date(appt.start_datetime).toLocaleString()}
              </p>
            </div>
            <span className="text-xs px-3 py-1 rounded-full bg-slate-800 border border-slate-700">{appt.status}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Appointments
