# Agent 2: ClickUp Task Management Integration

This agent fetches tasks from ClickUp and organizes them by employee for analysis and reporting.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install requests
```

### 2. Get ClickUp API Token
1. Go to [ClickUp Settings > Apps](https://app.clickup.com/settings/apps)
2. Click "Generate" to create a new API token
3. Copy the token (it starts with `pk_`)

### 3. Run Agent 2
```bash
python agent2_main.py
```

The script will guide you through:
- Entering your API token
- Selecting your team, space, and list
- Automatically fetching and organizing tasks

## 📁 Files

- `agent2_main.py` - Main script that orchestrates everything
- `fetch_clickup.py` - ClickUp API integration
- `organize_tasks.py` - Task organization and statistics
- `config.json` - Your workspace configuration (auto-generated)
- `summary_clickup.json` - Organized tasks by employee
- `clickup_statistics.json` - Detailed task statistics

## 🔧 Configuration

### Environment Variables (Optional)
```bash
export CLICKUP_API_TOKEN="your_token_here"
export CLICKUP_TEAM_ID="team_id"
export CLICKUP_SPACE_ID="space_id"
export CLICKUP_LIST_ID="list_id"
```

### Manual Configuration
Edit `config.json`:
```json
{
  "api_token": "pk_your_token_here",
  "team_id": "123456",
  "space_id": "789012",
  "list_id": "345678",
  "team_name": "Your Team",
  "space_name": "Your Space",
  "list_name": "Your List"
}
```

## 📊 Output

### Task Organization
Tasks are organized by employee with detailed information:
- Task name, description, status
- Due dates and completion dates
- Priority levels and tags
- Time estimates and time spent
- Custom fields

### Statistics Generated
- Total tasks per employee
- Completion rates
- Overdue tasks
- Tasks due soon
- Time tracking data

## 🔄 Integration with Other Agents

This agent outputs data in a format compatible with:
- **Agent 1**: Discord message analysis
- **Agent 3**: Final task analysis and reporting


## 🛠️ Troubleshooting

### Common Issues

1. **"No teams found"**
   - Check your API token
   - Ensure you have access to at least one team

2. **"No tasks found"**
   - Verify the selected list has tasks
   - Check if tasks are assigned to team members

3. **"Permission denied"**
   - Ensure your API token has read permissions
   - Check if you have access to the selected workspace

### API Rate Limits
ClickUp has rate limits. If you hit them:
- Wait a few minutes before retrying
- Consider using pagination for large datasets

## 📈 Features

- ✅ **Automatic Discovery**: Finds teams, spaces, and lists
- ✅ **Interactive Setup**: Guided configuration process
- ✅ **Rich Data**: Extracts all available task information
- ✅ **Statistics**: Comprehensive task analytics
- ✅ **Compatibility**: Works with existing agent system
- ✅ **Error Handling**: Robust error management
- ✅ **Flexible**: Works with any ClickUp workspace

## 🔗 ClickUp API Documentation

- [ClickUp API Docs](https://clickup.com/api)
- [Authentication](https://clickup.com/api/authentication)
- [Tasks Endpoint](https://clickup.com/api/clickupreference/operation/GetTasks)

## 📝 Example Usage

```python
from fetch_clickup import fetch_tasks_from_clickup
from organize_tasks import organize_tasks_by_employee

# Fetch tasks
tasks = fetch_tasks_from_clickup(api_token="pk_...", list_id="123456")

# Organize by employee
organized = organize_tasks_by_employee(tasks)

# Print results
for employee, emp_tasks in organized.items():
    print(f"{employee}: {len(emp_tasks)} tasks")
```
