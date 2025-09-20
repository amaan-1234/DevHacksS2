#!/usr/bin/env python3
"""
ClickUp Configuration
====================

Configuration file for ClickUp integration settings.
"""

# ClickUp API Configuration
CLICKUP_API_TOKEN = "YOUR_CLICKUP_API_TOKEN_HERE"  # Replace with your actual ClickUp API token

# Default workspace settings (will be auto-detected if not set)
DEFAULT_TEAM_ID = None
DEFAULT_SPACE_ID = None
DEFAULT_LIST_ID = None

# Task creation defaults
DEFAULT_PRIORITY = "Normal"  # Options: "Urgent", "High", "Normal", "Low"
DEFAULT_STATUS = "to do"     # Options: "to do", "in progress", "complete", "closed"

# Task field mappings
TASK_FIELDS = {
    "name": "name",
    "description": "description", 
    "status": "status",
    "priority": "priority",
    "assignees": "assignees",
    "due_date": "due_date",
    "tags": "tags"
}

# Status mappings for display
STATUS_MAPPING = {
    "to do": "📋 To Do",
    "in progress": "🔄 In Progress", 
    "complete": "✅ Complete",
    "closed": "🔒 Closed"
}

# Priority mappings for display
PRIORITY_MAPPING = {
    "urgent": "🚨 Urgent",
    "high": "🔴 High",
    "normal": "🟡 Normal", 
    "low": "🟢 Low"
}
