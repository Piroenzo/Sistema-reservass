import { Navigate } from 'react-router-dom'

const ProtectedRoute = ({ isAllowed, redirectTo = '/login', children }) => {
  if (!isAllowed) return <Navigate to={redirectTo} replace />
  return children
}

export default ProtectedRoute
