import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../api/axios'

const Register = () => {
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: '', email: '', password: '', role: 'client' })
  const [error, setError] = useState('')

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await api.post('/auth/register', form)
      navigate('/login')
    } catch (err) {
      setError(err.response?.data?.message || 'Error al registrar usuario')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-8 w-full max-w-md shadow-2xl">
        <h2 className="text-2xl font-bold mb-6 text-center">Crear cuenta</h2>
        {error && <p className="text-rose-500 text-sm mb-4">{error}</p>}
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="text-sm text-slate-300">Nombre</label>
            <input
              name="name"
              value={form.name}
              onChange={handleChange}
              className="mt-1 w-full rounded-lg bg-slate-800 border border-slate-700 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-rose-500"
              required
            />
          </div>
          <div>
            <label className="text-sm text-slate-300">Email</label>
            <input
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
              className="mt-1 w-full rounded-lg bg-slate-800 border border-slate-700 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-rose-500"
              required
            />
          </div>
          <div>
            <label className="text-sm text-slate-300">Contraseña</label>
            <input
              name="password"
              type="password"
              value={form.password}
              onChange={handleChange}
              className="mt-1 w-full rounded-lg bg-slate-800 border border-slate-700 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-rose-500"
              required
            />
          </div>
          <div>
            <label className="text-sm text-slate-300">Rol</label>
            <select
              name="role"
              value={form.role}
              onChange={handleChange}
              className="mt-1 w-full rounded-lg bg-slate-800 border border-slate-700 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-rose-500"
            >
              <option value="client">Cliente</option>
              <option value="owner">Propietario</option>
            </select>
          </div>
          <button type="submit" className="w-full py-2 rounded-lg bg-rose-600 hover:bg-rose-700 font-semibold">
            Registrarse
          </button>
        </form>
        <p className="mt-4 text-sm text-center text-slate-400">
          ¿Ya tenés cuenta?{' '}
          <Link to="/login" className="text-rose-400 hover:text-rose-300 font-semibold">
            Ingresá
          </Link>
        </p>
      </div>
    </div>
  )
}

export default Register
