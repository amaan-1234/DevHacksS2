import React, { useEffect, useState } from 'react'
import ClickUpSection from './components/ClickUpSection'
import TaskManagement from './components/TaskManagement'
import TeamLoadEqualizer from './components/TeamLoadEqualizer'

const fetchJSON = async (path) => {
  const res = await fetch(path)
  if (!res.ok) throw new Error(`Failed to load ${path}`)
  return res.json()
}

export default function App() {
  const [clickup, setClickup] = useState({ tasks: [], stats: null }) // ClickUp data
  const [error, setError] = useState(null)

  useEffect(() => {
    (async () => {
      try {
        const [a2tasks, a2stats] = await Promise.all([
          fetchJSON('/data/agent2_summary_clickup.json'),
          fetchJSON('/data/agent2_clickup_statistics.json'),
        ])
        // flatten ClickUp tasks from { employee: [tasks] }
        const flatTasks = Object.entries(a2tasks || {}).flatMap(([employee, tasks]) =>
          (tasks || []).map(t => ({ ...t, employee }))
        )
        setClickup({ tasks: flatTasks, stats: a2stats || null })
      } catch (e) {
        setError(e.message)
      }
    })()
  }, [])


  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: 16, maxWidth: 1200, margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center' }}>📋 ClickUp Task Management Dashboard</h1>
      <hr />

      {error && <div style={{ background: '#fee', border: '1px solid #f88', padding: 12, borderRadius: 8 }}>
        <b>Error:</b> {error}
      </div>}

      <TeamLoadEqualizer tasks={clickup.tasks} />
      <hr />
      <ClickUpSection tasks={clickup.tasks} stats={clickup.stats} />
      <hr />
      <TaskManagement
        onCreate={async (task) => {
          try {
            // Create task in ClickUp via proxy server
            const response = await fetch('http://localhost:4000/api/clickup/tasks', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                list_id: '901320275941', // Your ClickUp list ID
                name: task.name,
                description: task.description,
                assignees: [task.employee === 'Unassigned' ? null : task.employee].filter(Boolean),
                priority: task.priority === 'Urgent' ? 4 : task.priority === 'High' ? 3 : task.priority === 'Normal' ? 2 : 1,
                status: task.status,
                due_date: task.due_date ? new Date(task.due_date).getTime() : null
              })
            })
            
            if (response.ok) {
              const newTask = await response.json()
              // Add to local state for immediate UI update
              setClickup(prev => ({ ...prev, tasks: [{ ...task, id: newTask.id }, ...prev.tasks] }))
              alert('✅ Task created successfully in ClickUp!')
            } else {
              const error = await response.json()
              alert(`❌ Failed to create task: ${error.error || 'Unknown error'}`)
            }
          } catch (error) {
            console.error('Error creating task:', error)
            alert(`❌ Error creating task: ${error.message}`)
          }
        }}
        onUpdate={async (id, updates) => {
          try {
            const response = await fetch(`http://localhost:4000/api/clickup/tasks/${id}`, {
              method: 'PATCH',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(updates)
            })
            
            if (response.ok) {
              // Update local state for immediate UI update
              setClickup(prev => ({ ...prev, tasks: prev.tasks.map(t => t.id === id ? { ...t, ...updates } : t) }))
              alert('✅ Task updated successfully in ClickUp!')
            } else {
              const error = await response.json()
              alert(`❌ Failed to update task: ${error.error || 'Unknown error'}`)
            }
          } catch (error) {
            console.error('Error updating task:', error)
            alert(`❌ Error updating task: ${error.message}`)
          }
        }}
        onDelete={async (id) => {
          try {
            const response = await fetch(`http://localhost:4000/api/clickup/tasks/${id}`, {
              method: 'DELETE'
            })
            
            if (response.ok) {
              // Remove from local state for immediate UI update
              setClickup(prev => ({ ...prev, tasks: prev.tasks.filter(t => t.id !== id) }))
              alert('✅ Task deleted successfully from ClickUp!')
            } else {
              const error = await response.json()
              alert(`❌ Failed to delete task: ${error.error || 'Unknown error'}`)
            }
          } catch (error) {
            console.error('Error deleting task:', error)
            alert(`❌ Error deleting task: ${error.message}`)
          }
        }}
        employees={[...new Set(clickup.tasks.map(t => t.employee).filter(Boolean)), 'Unassigned']}
      />

      <p style={{ opacity: 0.7, marginTop: 24 }}>
        🔧 Built with React + Vite · 📊 Recharts · 💡 Loads sample JSON from <code>/public/data</code>. 
        ✅ ClickUp integration active via Node proxy at <code>localhost:4000</code>.
      </p>
    </div>
  )
}
