import React, { useMemo, useState } from 'react'

export default function TaskManagement({ onCreate, onUpdate, onDelete, employees }) {
  const [form, setForm] = useState({ name: '', description: '', employee: 'Unassigned', priority: 'Normal', status: 'to do', due_date: '' })

  return (
    <section>
      <h2>🎯 Task Management</h2>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16 }}>
        <div style={{ border: '1px solid #eee', borderRadius: 12, padding: 12 }}>
          <h3>➕ Create New Task</h3>
          <div style={{ display: 'grid', gap: 8 }}>
            <input placeholder="Task Name" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
            <textarea placeholder="Description" value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} />
            <div style={{ display: 'flex', gap: 8 }}>
              <label>Assign to:&nbsp;
                <select value={form.employee} onChange={e => setForm({ ...form, employee: e.target.value })}>
                  {employees.map(e => <option key={e}>{e}</option>)}
                </select>
              </label>
              <label>Priority:&nbsp;
                <select value={form.priority} onChange={e => setForm({ ...form, priority: e.target.value })}>
                  <option>Low</option><option>Normal</option><option>High</option><option>Urgent</option>
                </select>
              </label>
            </div>
            <div style={{ display: 'flex', gap: 8 }}>
              <label>Due Date:&nbsp;<input type="date" value={form.due_date} onChange={e => setForm({ ...form, due_date: e.target.value })} /></label>
              <label>Status:&nbsp;
                <select value={form.status} onChange={e => setForm({ ...form, status: e.target.value })}>
                  <option>to do</option><option>in progress</option><option>complete</option>
                </select>
              </label>
            </div>
            <button onClick={() => {
              if (!form.name.trim()) return alert('Please enter a task name')
              onCreate(form)
              setForm({ name: '', description: '', employee: 'Unassigned', priority: 'Normal', status: 'to do', due_date: '' })
            }}>🚀 Create Task</button>
          </div>
        </div>

        <div style={{ border: '1px solid #eee', borderRadius: 12, padding: 12 }}>
          <h3>⚙️ Actions (Update / Delete)</h3>
          <p>Use the task list in the ClickUp section to choose an item and copy its ID (if present), or target by exact name.</p>
          <UpdateDeleteForm onUpdate={onUpdate} onDelete={onDelete} />
        </div>
      </div>
    </section>
  )
}

function UpdateDeleteForm({ onUpdate, onDelete }) {
  const [id, setId] = useState('')
  const [name, setName] = useState('')
  const [status, setStatus] = useState('in progress')

  return (
    <div style={{ display: 'grid', gap: 8 }}>
      <input placeholder="Task ID (preferred)" value={id} onChange={e => setId(e.target.value)} />
      <input placeholder="...or Task Name (exact match)" value={name} onChange={e => setName(e.target.value)} />
      <label>Status:&nbsp;
        <select value={status} onChange={e => setStatus(e.target.value)}>
          <option>to do</option><option>in progress</option><option>complete</option>
        </select>
      </label>
      <div style={{ display: 'flex', gap: 8 }}>
        <button onClick={() => {
          if (!id && !name) return alert('Provide ID or exact Name')
          onUpdate(id || name, { status })
        }}>Update</button>

        <button onClick={() => {
          if (!id && !name) return alert('Provide ID or exact Name')
          onDelete(id || name)
        }}>Delete</button>
      </div>
    </div>
  )
}
