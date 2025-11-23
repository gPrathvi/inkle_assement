import React, { useEffect, useState } from 'react'
import { listPosts, createPost, likePost, unlikePost, me } from '../api'

export default function Feed() {
  const [posts, setPosts] = useState([])
  const [content, setContent] = useState('')
  const [meInfo, setMeInfo] = useState(null)
  const [error, setError] = useState('')

  async function refresh() {
    try {
      const [user, data] = await Promise.all([me(), listPosts()])
      setMeInfo(user)
      setPosts(Array.isArray(data) ? data : (data?.results || []))
    } catch (e) {
      setError(e?.response?.data?.detail || 'Failed to load feed')
    }
  }

  useEffect(() => {
    refresh()
  }, [])

  async function onPost(e) {
    e.preventDefault()
    if (!content.trim()) return
    await createPost(content.trim())
    setContent('')
    refresh()
  }

  async function onLike(p) {
    await likePost(p.id)
    refresh()
  }

  async function onUnlike(p) {
    await unlikePost(p.id)
    refresh()
  }

  return (
    <div className="feed">
      <div className="card">
        <h3>Hello {meInfo?.username || 'there'} 👋</h3>
        <form onSubmit={onPost} className="compose">
          <input value={content} onChange={e=>setContent(e.target.value)} placeholder="What's on your mind?" />
          <button type="submit">Post</button>
        </form>
      </div>
      {error && <p className="error">{error}</p>}
      {posts.map(p => (
        <div key={p.id} className="card">
          <div className="post-header">
            <strong>@{p.author_username || p.author?.username || 'user'}</strong>
          </div>
          <p>{p.content}</p>
          <div className="actions">
            <button onClick={() => onLike(p)}>Like</button>
            <button onClick={() => onUnlike(p)}>Unlike</button>
          </div>
        </div>
      ))}
    </div>
  )
}
