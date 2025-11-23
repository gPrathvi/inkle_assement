import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import App from './App'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Feed from './pages/Feed'
import './styles.css'

const root = createRoot(document.getElementById('root'))

function RequireAuth({ children }) {
  const token = localStorage.getItem('access')
  if (!token) return <Navigate to="/login" replace />
  return children
}

root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}> 
          <Route index element={<RequireAuth><Feed /></RequireAuth>} />
          <Route path="login" element={<Login />} />
          <Route path="signup" element={<Signup />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)
