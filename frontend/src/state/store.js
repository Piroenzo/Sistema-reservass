import { create } from 'zustand'
import api from '../api/axios'

const useAuthStore = create((set) => ({
  token: localStorage.getItem('token'),
  refreshToken: localStorage.getItem('refreshToken'),
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  setAuth: ({ token, refreshToken, user }) => {
    localStorage.setItem('token', token)
    localStorage.setItem('refreshToken', refreshToken)
    localStorage.setItem('user', JSON.stringify(user))
    set({ token, refreshToken, user })
  },
  logout: () => {
    localStorage.clear()
    set({ token: null, refreshToken: null, user: null })
  },
  refresh: async () => {
    const refreshToken = localStorage.getItem('refreshToken')
    if (!refreshToken) return
    const { data } = await api.post('/auth/refresh', {}, { headers: { Authorization: `Bearer ${refreshToken}` } })
    localStorage.setItem('token', data.access_token)
    set({ token: data.access_token })
  }
}))

export default useAuthStore
