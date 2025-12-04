import useAuthStore from '../state/store'

const Header = () => {
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)

  return (
    <header className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-900/80">
      <div>
        <h1 className="text-2xl font-bold">Turnos Pro</h1>
        <p className="text-sm text-slate-400">Sistema de reservas multi-negocio</p>
      </div>
      <div className="flex items-center gap-3">
        <div>
          <p className="font-semibold">{user?.name}</p>
          <p className="text-xs text-slate-400">{user?.role}</p>
        </div>
        <button
          onClick={logout}
          className="px-3 py-2 rounded-lg bg-rose-600 hover:bg-rose-700 text-sm font-semibold"
        >
          Salir
        </button>
      </div>
    </header>
  )
}

export default Header
