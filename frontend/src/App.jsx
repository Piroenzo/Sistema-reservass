import { Navigate, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import CalendarView from './pages/CalendarView'
import Services from './pages/Services'
import Professionals from './pages/Professionals'
import Clients from './pages/Clients'
import Appointments from './pages/Appointments'
import useAuthStore from './state/store'

function App() {
  const isAuthenticated = useAuthStore((state) => !!state.token)

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/"
        element={
          <ProtectedRoute isAllowed={isAuthenticated} redirectTo="/login">
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/calendar" element={<CalendarView />} />
        <Route path="/services" element={<Services />} />
        <Route path="/professionals" element={<Professionals />} />
        <Route path="/clients" element={<Clients />} />
        <Route path="/appointments" element={<Appointments />} />
      </Route>
    </Routes>
  )
}

export default App
