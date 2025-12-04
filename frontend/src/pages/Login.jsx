import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../api/axios'
import useAuthStore from '../state/store'

const Login = () => {
  const navigate = useNavigate()
  const setAuth = useAuthStore((state) => state.setAuth)
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const { data } = await api.post('/auth/login', form)
      setAuth({ token: data.access_token, refreshToken: data.refresh_token, user: data.user })
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.message || 'Error al iniciar sesión')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-8 w-full max-w-md shadow-2xl">
        <h2 className="text-2xl font-bold mb-6 text-center">Ingresar</h2>
        {error && <p className="text-rose-500 text-sm mb-4">{error}</p>}
        <form className="space-y-4" onSubmit={handleSubmit}>
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
          <button
            type="submit"
            className="w-full py-2 rounded-lg bg-rose-600 hover:bg-rose-700 font-semibold"
          >
            Entrar
          </button>
        </form>
        <p className="mt-4 text-sm text-center text-slate-400">
          ¿No tenés cuenta?{' '}
          <Link to="/register" className="text-rose-400 hover:text-rose-300 font-semibold">
            Registrate
          </Link>
        </p>
      </div>
    </div>
  )
}

export default Login
