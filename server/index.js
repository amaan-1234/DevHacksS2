import express from 'express'
import fetch from 'node-fetch'
import cors from 'cors'
import dotenv from 'dotenv'

// Load environment variables from .env file
dotenv.config()

const app = express()
app.use(cors())
app.use(express.json())

const CLICKUP_TOKEN = process.env.CLICKUP_API_TOKEN
console.log('CLICKUP_API_TOKEN:', CLICKUP_TOKEN ? 'SET' : 'NOT SET')

app.post('/api/clickup/tasks', async (req, res) => {
  if (!CLICKUP_TOKEN) return res.status(400).json({ error: 'CLICKUP_API_TOKEN not set' })
  const { list_id, ...payload } = req.body
  if (!list_id) return res.status(400).json({ error: 'list_id required' })
  try {
    const r = await fetch(`https://api.clickup.com/api/v2/list/${list_id}/task`, {
      method: 'POST',
      headers: { 'Authorization': CLICKUP_TOKEN, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await r.json()
    res.status(r.status).json(data)
  } catch (e) {
    res.status(500).json({ error: e.message })
  }
})

app.patch('/api/clickup/tasks/:taskId', async (req, res) => {
  if (!CLICKUP_TOKEN) return res.status(400).json({ error: 'CLICKUP_API_TOKEN not set' })
  const { taskId } = req.params
  try {
    const r = await fetch(`https://api.clickup.com/api/v2/task/${taskId}`, {
      method: 'PUT',
      headers: { 'Authorization': CLICKUP_TOKEN, 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body || {})
    })
    const data = await r.json()
    res.status(r.status).json(data)
  } catch (e) {
    res.status(500).json({ error: e.message })
  }
})

app.delete('/api/clickup/tasks/:taskId', async (req, res) => {
  if (!CLICKUP_TOKEN) return res.status(400).json({ error: 'CLICKUP_API_TOKEN not set' })
  const { taskId } = req.params
  try {
    const r = await fetch(`https://api.clickup.com/api/v2/task/${taskId}`, {
      method: 'DELETE',
      headers: { 'Authorization': CLICKUP_TOKEN }
    })
    if (r.status === 204) return res.json({ ok: true })
    const data = await r.json()
    res.status(r.status).json(data)
  } catch (e) {
    res.status(500).json({ error: e.message })
  }
})

const port = process.env.PORT || 4000
app.listen(port, () => console.log(`ClickUp proxy listening on :${port}`))
