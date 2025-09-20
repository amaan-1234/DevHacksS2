from collections import defaultdict
import json
from datetime import datetime


def organize_tasks_by_employee(clickup_tasks):
    """
    Organize ClickUp tasks by assignee/employee
    
    Args:
        clickup_tasks (list): List of ClickUp task dictionaries
    
    Returns:
        dict: Tasks organized by employee name
    """
    employee_tasks = defaultdict(list)
    
    for task in clickup_tasks:
        # Skip if task is None or not a dictionary
        if not task or not isinstance(task, dict):
            print(f"⚠️ Skipping invalid task: {task}")
            continue
            
        # Extract assignee information
        assignees = task.get("assignees", [])
        if assignees and len(assignees) > 0:
            # ClickUp can have multiple assignees, we'll use the first one
            assignee = assignees[0].get("username", "Unknown")
        else:
            assignee = "Unassigned"
        
        # Extract task information
        status_obj = task.get("status", {})
        priority_obj = task.get("priority", {})
        
        task_info = {
            "id": task.get("id", ""),
            "name": task.get("name", "Untitled Task"),
            "description": task.get("description", ""),
            "status": status_obj.get("status", "Unknown") if status_obj else "Unknown",
            "priority": priority_obj.get("priority", "Normal") if priority_obj else "Normal",
            "due_date": task.get("due_date"),
            "date_created": task.get("date_created"),
            "date_updated": task.get("date_updated"),
            "date_closed": task.get("date_closed"),
            "url": task.get("url", ""),
            "tags": [tag.get("name", "") for tag in task.get("tags", []) if tag],
            "time_estimate": task.get("time_estimate"),
            "time_spent": task.get("time_spent"),
            "creator": task.get("creator", {}).get("username", "Unknown") if task.get("creator") else "Unknown"
        }
        
        # Add custom fields if they exist
        custom_fields = task.get("custom_fields", [])
        if custom_fields:
            task_info["custom_fields"] = {}
            for field in custom_fields:
                field_name = field.get("name", "Unknown Field")
                field_value = field.get("value", "")
                task_info["custom_fields"][field_name] = field_value
        
        employee_tasks[assignee].append(task_info)
    
    return dict(employee_tasks)


def get_task_statistics(employee_tasks):
    """
    Generate statistics for the organized tasks
    
    Args:
        employee_tasks (dict): Tasks organized by employee
    
    Returns:
        dict: Statistics summary
    """
    stats = {
        "total_employees": len(employee_tasks),
        "total_tasks": 0,
        "employee_stats": {}
    }
    
    for employee, tasks in employee_tasks.items():
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t.get("status", "").lower() in ["complete", "done", "closed"]])
        overdue_tasks = 0
        due_soon_tasks = 0
        
        # Check for overdue and due soon tasks
        current_date = datetime.now()
        for task in tasks:
            due_date = task.get("due_date")
            if due_date:
                try:
                    due_datetime = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                    if due_datetime < current_date and task.get("status", "").lower() not in ["complete", "done", "closed"]:
                        overdue_tasks += 1
                    elif (due_datetime - current_date).days <= 7 and task.get("status", "").lower() not in ["complete", "done", "closed"]:
                        due_soon_tasks += 1
                except:
                    pass  # Skip if date parsing fails
        
        stats["employee_stats"][employee] = {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": total_tasks - completed_tasks,
            "overdue_tasks": overdue_tasks,
            "due_soon_tasks": due_soon_tasks,
            "completion_rate": round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2)
        }
        
        stats["total_tasks"] += total_tasks
    
    return stats


def save_organized_tasks(employee_tasks, filename="summary_clickup.json"):
    """
    Save organized tasks to JSON file
    
    Args:
        employee_tasks (dict): Tasks organized by employee
        filename (str): Output filename
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(employee_tasks, f, indent=2, ensure_ascii=False)
    print(f"✅ Organized tasks saved to {filename}")


def save_task_statistics(stats, filename="clickup_statistics.json"):
    """
    Save task statistics to JSON file
    
    Args:
        stats (dict): Task statistics
        filename (str): Output filename
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"✅ Task statistics saved to {filename}")


# ---------------- Test ----------------
if __name__ == "__main__":
    # Mock ClickUp task data for testing
    mock_clickup_tasks = [
        {
            "id": "task_1",
            "name": "Fix login bug",
            "description": "Fix the login issue reported by users",
            "status": {"status": "in progress"},
            "priority": {"priority": "high"},
            "assignees": [{"username": "alice_dev"}],
            "due_date": "2024-12-31T23:59:59.000Z",
            "date_created": "2024-01-01T00:00:00.000Z",
            "date_updated": "2024-01-15T00:00:00.000Z",
            "date_closed": None,
            "url": "https://app.clickup.com/t/task_1",
            "tags": [{"name": "bug"}, {"name": "frontend"}],
            "time_estimate": 3600000,  # 1 hour in milliseconds
            "time_spent": 1800000,     # 30 minutes in milliseconds
            "custom_fields": []
        },
        {
            "id": "task_2", 
            "name": "Update documentation",
            "description": "Update API documentation",
            "status": {"status": "complete"},
            "priority": {"priority": "normal"},
            "assignees": [{"username": "bob_writer"}],
            "due_date": "2024-01-15T23:59:59.000Z",
            "date_created": "2024-01-01T00:00:00.000Z",
            "date_updated": "2024-01-14T00:00:00.000Z",
            "date_closed": "2024-01-14T00:00:00.000Z",
            "url": "https://app.clickup.com/t/task_2",
            "tags": [{"name": "documentation"}],
            "time_estimate": 7200000,  # 2 hours
            "time_spent": 7200000,     # 2 hours
            "custom_fields": []
        },
        {
            "id": "task_3",
            "name": "Code review",
            "description": "Review pull request #123",
            "status": {"status": "open"},
            "priority": {"priority": "low"},
            "assignees": [],  # Unassigned
            "due_date": "2024-12-25T23:59:59.000Z",
            "date_created": "2024-01-10T00:00:00.000Z",
            "date_updated": "2024-01-10T00:00:00.000Z",
            "date_closed": None,
            "url": "https://app.clickup.com/t/task_3",
            "tags": [{"name": "review"}],
            "time_estimate": 1800000,  # 30 minutes
            "time_spent": 0,
            "custom_fields": []
        }
    ]
    
    print("🧪 Testing ClickUp task organization...")
    
    # Organize tasks by employee
    organized_tasks = organize_tasks_by_employee(mock_clickup_tasks)
    print(f"\n📊 Organized tasks for {len(organized_tasks)} employees:")
    for employee, tasks in organized_tasks.items():
        print(f"  {employee}: {len(tasks)} tasks")
    
    # Generate statistics
    stats = get_task_statistics(organized_tasks)
    print(f"\n📈 Task Statistics:")
    print(f"  Total employees: {stats['total_employees']}")
    print(f"  Total tasks: {stats['total_tasks']}")
    
    for employee, emp_stats in stats['employee_stats'].items():
        print(f"\n  {employee}:")
        print(f"    Total: {emp_stats['total_tasks']}")
        print(f"    Completed: {emp_stats['completed_tasks']}")
        print(f"    Pending: {emp_stats['pending_tasks']}")
        print(f"    Overdue: {emp_stats['overdue_tasks']}")
        print(f"    Due Soon: {emp_stats['due_soon_tasks']}")
        print(f"    Completion Rate: {emp_stats['completion_rate']}%")
    
    # Save results
    save_organized_tasks(organized_tasks)
    save_task_statistics(stats)
    
    print("\n✅ Test completed successfully!")
