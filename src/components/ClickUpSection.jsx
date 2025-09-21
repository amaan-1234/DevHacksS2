import React, { useMemo, useState } from 'react'
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend } from 'recharts'

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#a4de6c', '#d0ed57']

export default function ClickUpSection({ tasks, stats }) {
  const [filters, setFilters] = useState({ status: 'All', priority: 'All', employee: 'All' })

  const statusCounts = useMemo(() => {
    const m = new Map()
    tasks.forEach(t => m.set(t.status, (m.get(t.status) || 0) + 1))
    return Array.from(m, ([name, value]) => ({ name, value }))
  }, [tasks])

  const tasksByEmployee = useMemo(() => {
    const m = new Map()
    tasks.forEach(t => m.set(t.employee || 'Unassigned', (m.get(t.employee || 'Unassigned') || 0) + 1))
    return Array.from(m, ([employee, count]) => ({ employee, count }))
  }, [tasks])

  const employees = useMemo(() => Array.from(new Set(tasks.map(t => t.employee || 'Unassigned'))), [tasks])
  const statuses = useMemo(() => Array.from(new Set(tasks.map(t => t.status))), [tasks])
  const priorities = useMemo(() => Array.from(new Set(tasks.map(t => t.priority || 'None'))), [tasks])

  const filtered = useMemo(() => {
    return tasks.filter(t => 
      (filters.status === 'All' || t.status === filters.status) &&
      (filters.priority === 'All' || (t.priority || 'None') === filters.priority) &&
      (filters.employee === 'All' || (t.employee || 'Unassigned') === filters.employee)
    )
  }, [tasks, filters])

  return (
    <section>
      <h2>📊 ClickUp Task Analytics</h2>
      <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
        <div style={{ flex: '1 1 320px', minWidth: 320, height: 300, border: '1px solid #eee', borderRadius: 12, padding: 8 }}>
          <h3 style={{ margin: 8 }}>Task Status Distribution</h3>
          <ResponsiveContainer width="100%" height="85%">
            <PieChart>
              <Pie dataKey="value" data={statusCounts} outerRadius={100} label>
                {statusCounts.map((entry, index) => <Cell key={`cell-${index}`} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div style={{ flex: '1 1 420px', minWidth: 420, height: 300, border: '1px solid #eee', borderRadius: 12, padding: 8 }}>
          <h3 style={{ margin: 8 }}>Tasks by Employee</h3>
          <ResponsiveContainer width="100%" height="85%">
            <BarChart data={tasksByEmployee}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="employee" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div style={{ marginTop: 16, display: 'flex', gap: 12, flexWrap: 'wrap' }}>
        <label>Filter by Status:&nbsp;
          <select value={filters.status} onChange={e => setFilters({ ...filters, status: e.target.value })}>
            <option>All</option>
            {statuses.map(s => <option key={s}>{s}</option>)}
          </select>
        </label>
        <label>Filter by Priority:&nbsp;
          <select value={filters.priority} onChange={e => setFilters({ ...filters, priority: e.target.value })}>
            <option>All</option>
            {priorities.map(p => <option key={p}>{p}</option>)}
          </select>
        </label>
        <label>Filter by Employee:&nbsp;
          <select value={filters.employee} onChange={e => setFilters({ ...filters, employee: e.target.value })}>
            <option>All</option>
            {employees.map(emp => <option key={emp}>{emp}</option>)}
          </select>
        </label>
      </div>

      <div style={{ marginTop: 12 }}>
        {filtered.length === 0 ? <i>No tasks match filters.</i> : null}
        {filtered.map(t => (
          <details key={(t.id || '') + (t.name || '')} style={{ marginBottom: 8, border: '1px solid #eee', borderRadius: 8, padding: 8 }}>
            <summary>
              📝 <b>{t.name || 'Untitled'}</b> — <i>{t.status || 'Unknown'}</i>
            </summary>
            <div style={{ marginTop: 8, fontSize: 14 }}>
              <div><b>Description:</b> {t.description || '—'}</div>
              <div><b>Priority:</b> {t.priority || '—'}</div>
              <div><b>Employee:</b> {t.employee || 'Unassigned'}</div>
              <div><b>Created:</b> {t.date_created ? new Date(Number(t.date_created)).toLocaleString() : '—'}</div>
              <div><b>Updated:</b> {t.date_updated ? new Date(Number(t.date_updated)).toLocaleString() : '—'}</div>
              <div><b>Due:</b> {t.due_date ? (isNaN(t.due_date) ? t.due_date : new Date(Number(t.due_date)).toLocaleDateString()) : '—'}</div>
              {t.url && <div><a href={t.url} target="_blank" rel="noreferrer">Open in ClickUp</a></div>}
            </div>
          </details>
        ))}
      </div>
    </section>
  )
}
