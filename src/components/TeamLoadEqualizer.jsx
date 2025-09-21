// src/components/TeamLoadEqualizer.jsx
import React, { useMemo } from 'react'

// Generate team workload data based on ClickUp tasks
const generateTeamWorkloadData = (tasks) => {
  // Default team members (User 1 to User 5)
  const teamMembers = ['User 1', 'User 2', 'User 3', 'User 4', 'User 5']
  const teamWorkload = {}
  
  if (!tasks || tasks.length === 0) {
    // Start with 0 tasks for all users
    teamMembers.forEach(member => {
      teamWorkload[member] = {
        workload: 0,
        status: 'Available',
        tasks: 0,
        color: 'green'
      }
    })
  } else {
    // Calculate workload based on actual ClickUp data
    const employeeStats = {}
    tasks.forEach(task => {
      const emp = task.employee || 'Unassigned'
      if (emp !== 'Unassigned') {
        employeeStats[emp] = (employeeStats[emp] || 0) + 1
      }
    })
    
    // Only count assigned tasks (exclude 'Unassigned')
    const assignedTasks = tasks.filter(task => task.employee && task.employee !== 'Unassigned')
    const totalTasks = assignedTasks.length
    
    // Calculate workload for each user
    teamMembers.forEach(member => {
      // Check if this user has tasks in ClickUp data
      const taskCount = employeeStats[member] || 0
      
      // Calculate workload as percentage of total tasks
      let workload = 0
      if (totalTasks > 0) {
        workload = Math.min(95, (taskCount / totalTasks) * 100)
      }
      
      // Determine status and color based on workload
      let status, color
      if (workload >= 90) {
        status = 'Overloaded'
        color = 'red'
      } else if (workload >= 70) {
        status = 'In Focus'
        color = 'orange'
      } else if (workload >= 40) {
        status = 'Balanced'
        color = 'green'
      } else {
        status = 'Available'
        color = 'green'
      }
      
      teamWorkload[member] = {
        workload: Math.round(workload),
        status,
        tasks: taskCount,
        color
      }
    })
  }
  
  return teamWorkload
}

const getBalancingSuggestion = (teamWorkload) => {
  const overloaded = Object.entries(teamWorkload).filter(([_, data]) => data.status === 'Overloaded')
  const available = Object.entries(teamWorkload).filter(([_, data]) => data.status === 'Available')
  const inFocus = Object.entries(teamWorkload).filter(([_, data]) => data.status === 'In Focus')
  const balanced = Object.entries(teamWorkload).filter(([_, data]) => data.status === 'Balanced')
  
  // Check if all users have 0 tasks
  const totalTasks = Object.values(teamWorkload).reduce((sum, data) => sum + data.tasks, 0)
  
  if (totalTasks === 0) {
    return "All team members are available. Start assigning tasks to see workload distribution!"
  } else if (overloaded.length > 0 && available.length > 0) {
    return `${overloaded[0][0]} has a high workload. Consider reassigning some tasks to ${available[0][0]} to balance the team.`
  } else if (overloaded.length > 0 && inFocus.length > 0) {
    return `${overloaded[0][0]} is overloaded. Consider redistributing tasks to ${inFocus[0][0]} or other team members.`
  } else if (overloaded.length > 0) {
    return `${overloaded[0][0]} is overloaded. Consider redistributing tasks among team members.`
  } else if (available.length > 0) {
    return `${available[0][0]} is available and can take on more tasks to help balance the team workload.`
  } else {
    return "Team workload is well balanced. Great job!"
  }
}

const getStatusIcon = (status) => {
  switch (status) {
    case 'Overloaded':
      return '🔴'
    case 'In Focus':
      return '🟠'
    case 'Balanced':
      return '🟢'
    default:
      return '🟢'
  }
}

const getStatusColor = (status) => {
  switch (status) {
    case 'Overloaded':
      return '#ef4444'
    case 'In Focus':
      return '#f59e0b'
    case 'Balanced':
      return '#10b981'
    default:
      return '#3b82f6'
  }
}

export default function TeamLoadEqualizer({ tasks }) {
  const teamWorkload = useMemo(() => generateTeamWorkloadData(tasks), [tasks])
  const suggestion = useMemo(() => getBalancingSuggestion(teamWorkload), [teamWorkload])

  return (
    <section>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h2 style={{ margin: 0 }}>⚖️ Team Workload Equalizer</h2>
        <button 
          onClick={() => window.location.reload()} 
          style={{
            background: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: 6,
            padding: '8px 16px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: 8
          }}
        >
          🔄 Refresh Workload
        </button>
      </div>
      
      <h3 style={{ marginTop: 0, marginBottom: 16 }}>Team Workload Balance</h3>
      
      {/* Display team workload bars */}
      {Object.entries(teamWorkload).map(([member, data]) => (
        <div key={member} style={{ 
          display: 'flex', 
          alignItems: 'center', 
          marginBottom: 16,
          gap: 16
        }}>
          {/* User name */}
          <div style={{ width: 120, fontWeight: 'bold' }}>
            {member}
          </div>
          
          {/* Progress bar */}
          <div style={{ flex: 1, position: 'relative' }}>
            <div style={{
              width: '100%',
              height: 24,
              backgroundColor: '#e5e7eb',
              borderRadius: 12,
              overflow: 'hidden',
              position: 'relative'
            }}>
              <div style={{
                width: `${data.workload}%`,
                height: '100%',
                backgroundColor: getStatusColor(data.status),
                transition: 'width 0.3s ease',
                borderRadius: 12
              }} />
            </div>
            <div style={{ 
              marginTop: 4, 
              fontSize: 14, 
              color: '#6b7280',
              textAlign: 'center'
            }}>
              {data.status} • {data.tasks} tasks
            </div>
          </div>
          
          {/* Status indicator */}
          <div style={{
            width: 120,
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            padding: '6px 12px',
            borderRadius: 6,
            backgroundColor: getStatusColor(data.status),
            color: 'white',
            fontSize: 14,
            fontWeight: 'bold'
          }}>
            {getStatusIcon(data.status)} {data.status}
          </div>
        </div>
      ))}
      
      {/* Balancing suggestion */}
      <div style={{ marginTop: 24 }}>
        <h3 style={{ marginBottom: 12, display: 'flex', alignItems: 'center', gap: 8 }}>
          💡 Balancing Suggestion
        </h3>
        <div style={{
          backgroundColor: '#dbeafe',
          border: '1px solid #3b82f6',
          borderRadius: 8,
          padding: 16,
          color: '#1e40af'
        }}>
          ⚡ {suggestion}
        </div>
      </div>
    </section>
  )
}
