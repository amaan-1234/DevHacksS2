#!/usr/bin/env python3
"""
Agent 2: ClickUp Task Management Integration
===========================================

This script fetches tasks from ClickUp and organizes them by employee.
It's designed to work as part of the multi-agent system for task management.

Usage:
    python agent2_main.py

Requirements:
    - ClickUp API token
    - requests library
    - Valid ClickUp workspace with tasks
"""

import json
import sys
import os
from datetime import datetime

# Import our custom modules
from fetch_clickup import fetch_tasks_from_clickup, get_team_info, get_spaces_from_team, get_lists_from_space
from organize_tasks import organize_tasks_by_employee, get_task_statistics, save_organized_tasks, save_task_statistics


def load_config():
    """Load configuration from config.json or environment variables"""
    config_file = "config.json"
    
    # Try to load from config file first
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                print("✅ Loaded configuration from config.json")
                return config
        except Exception as e:
            print(f"⚠️ Error loading config.json: {e}")
    
    # Fallback to environment variables
    config = {
        "api_token": os.getenv("CLICKUP_API_TOKEN"),
        "team_id": os.getenv("CLICKUP_TEAM_ID"),
        "space_id": os.getenv("CLICKUP_SPACE_ID"),
        "list_id": os.getenv("CLICKUP_LIST_ID")
    }
    
    if config["api_token"]:
        print("✅ Loaded configuration from environment variables")
    else:
        print("⚠️ No configuration found")
    
    return config


def save_config(config):
    """Save configuration to config.json"""
    with open("config.json", 'w') as f:
        json.dump(config, f, indent=2)
    print("✅ Configuration saved to config.json")


def setup_clickup_workspace(api_token):
    """Interactive setup to discover and configure ClickUp workspace"""
    print("\n🔧 ClickUp Workspace Setup")
    print("=" * 40)
    
    # Get teams
    print("📋 Discovering teams...")
    teams = get_team_info(api_token)
    
    if not teams:
        print("❌ No teams found. Please check your API token.")
        return None
    
    # Auto-select first team
    print(f"\n📊 Found {len(teams)} team(s):")
    for i, team in enumerate(teams):
        print(f"  {i+1}. {team['name']} (ID: {team['id']})")
    
    # Auto-select first team
    selected_team = teams[0]
    print(f"\n✅ Auto-selected team: {selected_team['name']}")
    
    print(f"✅ Selected team: {selected_team['name']}")
    
    # Get spaces
    print(f"\n📁 Discovering spaces in team '{selected_team['name']}'...")
    spaces = get_spaces_from_team(api_token, selected_team['id'])
    
    if not spaces:
        print("❌ No spaces found in this team.")
        return None
    
    # Auto-select first space
    print(f"\n📊 Found {len(spaces)} space(s):")
    for i, space in enumerate(spaces):
        print(f"  {i+1}. {space['name']} (ID: {space['id']})")
    
    # Auto-select first space
    selected_space = spaces[0]
    print(f"\n✅ Auto-selected space: {selected_space['name']}")
    
    print(f"✅ Selected space: {selected_space['name']}")
    
    # Get lists
    print(f"\n📋 Discovering lists in space '{selected_space['name']}'...")
    lists = get_lists_from_space(api_token, selected_space['id'])
    
    if not lists:
        print("❌ No lists found in this space.")
        return None
    
    # Auto-select first list
    print(f"\n📊 Found {len(lists)} list(s):")
    for i, list_item in enumerate(lists):
        print(f"  {i+1}. {list_item['name']} (ID: {list_item['id']})")
    
    # Auto-select first list
    selected_list = lists[0]
    print(f"\n✅ Auto-selected list: {selected_list['name']}")
    
    print(f"✅ Selected list: {selected_list['name']}")
    
    # Save configuration
    config = {
        "api_token": api_token,
        "team_id": selected_team['id'],
        "space_id": selected_space['id'],
        "list_id": selected_list['id'],
        "team_name": selected_team['name'],
        "space_name": selected_space['name'],
        "list_name": selected_list['name']
    }
    
    save_config(config)
    return config


def main():
    """Main function to run Agent 2"""
    print("🤖 Agent 2: ClickUp Task Management")
    print("=" * 50)
    
    # Load configuration
    config = load_config()
    
    # Check if we have API token
    if not config.get("api_token"):
        # Use the provided API token
        config["api_token"] = "YOUR_CLICKUP_API_TOKEN_HERE"
        print("✅ Using provided ClickUp API token")
    
    # Setup workspace if needed
    if not config.get("list_id"):
        print("\n🔧 No workspace configuration found. Let's set it up!")
        config = setup_clickup_workspace(config["api_token"])
        if not config:
            print("❌ Setup failed. Exiting.")
            return
    
    print(f"\n📊 Using workspace:")
    print(f"  Team: {config.get('team_name', 'Unknown')}")
    print(f"  Space: {config.get('space_name', 'Unknown')}")
    print(f"  List: {config.get('list_name', 'Unknown')}")
    
    # Fetch tasks from ClickUp
    print(f"\n📥 Fetching tasks from ClickUp...")
    tasks = fetch_tasks_from_clickup(
        api_token=config["api_token"],
        list_id=config["list_id"]
    )
    
    if not tasks:
        print("❌ No tasks found or error occurred.")
        return
    
    print(f"✅ Successfully fetched {len(tasks)} tasks")
    
    # Organize tasks by employee
    print(f"\n📊 Organizing tasks by employee...")
    organized_tasks = organize_tasks_by_employee(tasks)
    
    print(f"✅ Organized tasks for {len(organized_tasks)} employees:")
    for employee, emp_tasks in organized_tasks.items():
        print(f"  {employee}: {len(emp_tasks)} tasks")
    
    # Generate statistics
    print(f"\n📈 Generating task statistics...")
    stats = get_task_statistics(organized_tasks)
    
    print(f"\n📊 Summary Statistics:")
    print(f"  Total employees: {stats['total_employees']}")
    print(f"  Total tasks: {stats['total_tasks']}")
    
    # Show detailed stats for each employee
    for employee, emp_stats in stats['employee_stats'].items():
        print(f"\n  👤 {employee}:")
        print(f"    📋 Total tasks: {emp_stats['total_tasks']}")
        print(f"    ✅ Completed: {emp_stats['completed_tasks']}")
        print(f"    ⏳ Pending: {emp_stats['pending_tasks']}")
        print(f"    ⚠️ Overdue: {emp_stats['overdue_tasks']}")
        print(f"    🔔 Due soon: {emp_stats['due_soon_tasks']}")
        print(f"    📊 Completion rate: {emp_stats['completion_rate']}%")
    
    # Save results
    print(f"\n💾 Saving results...")
    save_organized_tasks(organized_tasks, "summary_clickup.json")
    save_task_statistics(stats, "clickup_statistics.json")
    
    
    print(f"\n🎉 Agent 2 completed successfully!")
    print(f"📁 Output files:")
    print(f"  - summary_clickup.json (organized tasks)")
    print(f"  - clickup_statistics.json (detailed statistics)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
