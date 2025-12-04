import { NavLink } from 'react-router-dom'

const links = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/calendar', label: 'Calendario' },
  { to: '/appointments', label: 'Turnos' },
  { to: '/services', label: 'Servicios' },
  { to: '/professionals', label: 'Profesionales' },
  { to: '/clients', label: 'Clientes' }
]

const Sidebar = () => {
  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 p-4 space-y-4 hidden md:block">
      <h2 className="text-lg font-semibold text-slate-300">Menú</h2>
      <nav className="space-y-2">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `block px-3 py-2 rounded-lg text-sm font-semibold transition ${
                isActive ? 'bg-slate-800 text-white' : 'text-slate-400 hover:text-white hover:bg-slate-800'
              }`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar
