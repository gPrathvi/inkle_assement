import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { signup, login } from '../api'

export default function Signup() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  async function onSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      await signup({ username, email, password })
      await login({ username, password })
      navigate('/')
    } catch (err) {
      setError(err?.response?.data?.detail || 'Signup failed')
    }
  }

  return (
    <div className="card">
      <h2>Signup</h2>
      <form onSubmit={onSubmit}>
        <input placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button type="submit">Create account</button>
      </form>
      {error && <p className="error">{error}</p>}
      <p>Already have an account? <Link to="/login">Login</Link></p>
    </div>
  )
}
