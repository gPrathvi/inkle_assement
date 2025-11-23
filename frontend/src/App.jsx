import React from 'react'
import { Link, Outlet, useNavigate } from 'react-router-dom'

export default function App() {
  const navigate = useNavigate()
  const token = localStorage.getItem('access')

  function logout() {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
    navigate('/login')
  }

  return (
    <div className="container">
      <header className="topbar">
        <h1>Inkle</h1>
        <nav>
          {!token ? (
            <>
              <Link to="/login">Login</Link>
              <Link to="/signup">Signup</Link>
            </>
          ) : (
            <>
              <Link to="/">Feed</Link>
              <button onClick={logout}>Logout</button>
            </>
          )}
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  )
}
