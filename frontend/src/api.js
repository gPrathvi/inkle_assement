import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000',
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export async function signup({ username, email, password }) {
  const { data } = await api.post('/api/auth/signup/', { username, email, password })
  return data
}

export async function login({ username, password }) {
  const { data } = await api.post('/api/auth/login/', { username, password })
  // expecting data.access and data.refresh
  if (data.access) localStorage.setItem('access', data.access)
  if (data.refresh) localStorage.setItem('refresh', data.refresh)
  return data
}

export async function me() {
  const { data } = await api.get('/api/users/me/')
  return data
}

export async function listPosts() {
  const { data } = await api.get('/api/posts/')
  return data
}

export async function createPost(content) {
  const { data } = await api.post('/api/posts/', { content })
  return data
}

export async function likePost(postId) {
  const { data } = await api.post(`/api/posts/${postId}/like/`)
  return data
}

export async function unlikePost(postId) {
  const { data } = await api.post(`/api/posts/${postId}/unlike/`)
  return data
}

export default api
