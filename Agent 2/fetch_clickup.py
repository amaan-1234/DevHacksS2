import requests
import json
from datetime import datetime


def fetch_tasks_from_clickup(api_token, team_id=None, space_id=None, list_id=None):
    """
    Fetch tasks from ClickUp API
    
    Args:
        api_token (str): ClickUp API token
        team_id (str): Optional team ID to filter tasks
        space_id (str): Optional space ID to filter tasks  
        list_id (str): Optional list ID to filter tasks
    
    Returns:
        list: List of task dictionaries
    """
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }
    
    # Base URL for ClickUp API
    base_url = "https://api.clickup.com/api/v2"
    
    # Build the endpoint based on what IDs are provided
    if list_id:
        endpoint = f"{base_url}/list/{list_id}/task"
    elif space_id:
        endpoint = f"{base_url}/space/{space_id}/task"
    elif team_id:
        endpoint = f"{base_url}/team/{team_id}/task"
    else:
        # If no specific ID, get all tasks (requires team_id)
        print("❌ Error: At least team_id is required")
        return []
    
    print(f"\n📡 Fetching tasks from ClickUp API...")
    print(f"🔗 Endpoint: {endpoint}")
    
    try:
        response = requests.get(endpoint, headers=headers)
        print(f"📥 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            tasks = data.get('tasks', [])
            print(f"✅ Successfully fetched {len(tasks)} tasks")
            return tasks
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        return []


def get_team_info(api_token):
    """Get team information to help with setup"""
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get("https://api.clickup.com/api/v2/team", headers=headers)
        if response.status_code == 200:
            teams = response.json().get('teams', [])
            print(f"✅ Found {len(teams)} teams:")
            for team in teams:
                print(f"  - Team ID: {team['id']}, Name: {team['name']}")
            return teams
        else:
            print(f"❌ Error getting teams: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


def get_spaces_from_team(api_token, team_id):
    """Get spaces from a specific team"""
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"https://api.clickup.com/api/v2/team/{team_id}/space", headers=headers)
        if response.status_code == 200:
            spaces = response.json().get('spaces', [])
            print(f"✅ Found {len(spaces)} spaces in team {team_id}:")
            for space in spaces:
                print(f"  - Space ID: {space['id']}, Name: {space['name']}")
            return spaces
        else:
            print(f"❌ Error getting spaces: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


def get_lists_from_space(api_token, space_id):
    """Get lists from a specific space"""
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"https://api.clickup.com/api/v2/space/{space_id}/list", headers=headers)
        if response.status_code == 200:
            lists = response.json().get('lists', [])
            print(f"✅ Found {len(lists)} lists in space {space_id}:")
            for list_item in lists:
                print(f"  - List ID: {list_item['id']}, Name: {list_item['name']}")
            return lists
        else:
            print(f"❌ Error getting lists: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []


# ---------------- Test ----------------
if __name__ == "__main__":
    # Replace with your ClickUp API token
    API_TOKEN = "pk_168045299_J7COUYH125ABZ9K363BYCRPV9SHDUTWL"
    
    if API_TOKEN == "YOUR_CLICKUP_API_TOKEN_HERE":
        print("❌ Please set your ClickUp API token in the API_TOKEN variable")
        print("📝 Get your API token from: https://app.clickup.com/settings/apps")
        exit(1)
    
    # First, let's see what teams are available
    print("🔍 Getting team information...")
    teams = get_team_info(API_TOKEN)
    
    if teams:
        # Use the first team for demonstration
        team_id = teams[0]['id']
        print(f"\n🔍 Getting spaces for team: {teams[0]['name']}")
        spaces = get_spaces_from_team(API_TOKEN, team_id)
        
        if spaces:
            # Use the first space for demonstration
            space_id = spaces[0]['id']
            print(f"\n🔍 Getting lists for space: {spaces[0]['name']}")
            lists = get_lists_from_space(API_TOKEN, space_id)
            
            if lists:
                # Fetch tasks from the first list
                list_id = lists[0]['id']
                print(f"\n📋 Fetching tasks from list: {lists[0]['name']}")
                tasks = fetch_tasks_from_clickup(API_TOKEN, team_id=team_id, list_id=list_id)
                
                if tasks:
                    print(f"\n✅ Sample task data:")
                    for i, task in enumerate(tasks[:3]):  # Show first 3 tasks
                        print(f"  Task {i+1}: {task.get('name', 'No name')} - Status: {task.get('status', {}).get('status', 'Unknown')}")
            else:
                print("❌ No lists found in the space")
        else:
            print("❌ No spaces found in the team")
    else:
        print("❌ No teams found. Please check your API token and try again.")


def create_task_in_clickup(api_token, list_id, task_data):
    """
    Create a new task in ClickUp
    
    Args:
        api_token (str): ClickUp API token
        list_id (str): List ID where task will be created
        task_data (dict): Task data including name, description, assignees, etc.
    
    Returns:
        dict: Created task data or None if failed
    """
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }
    
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    
    try:
        response = requests.post(url, headers=headers, json=task_data)
        response.raise_for_status()
        
        task = response.json()
        print(f"✅ Task created successfully: {task.get('name', 'Unknown')}")
        return task
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating task: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
        return None


def update_task_in_clickup(api_token, task_id, task_data):
    """
    Update an existing task in ClickUp
    
    Args:
        api_token (str): ClickUp API token
        task_id (str): Task ID to update
        task_data (dict): Updated task data
    
    Returns:
        dict: Updated task data or None if failed
    """
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }
    
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    
    try:
        response = requests.put(url, headers=headers, json=task_data)
        response.raise_for_status()
        
        task = response.json()
        print(f"✅ Task updated successfully: {task.get('name', 'Unknown')}")
        return task
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error updating task: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None


def delete_task_in_clickup(api_token, task_id):
    """
    Delete a task in ClickUp
    
    Args:
        api_token (str): ClickUp API token
        task_id (str): Task ID to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    headers = {
        "Authorization": api_token
    }
    
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        
        print(f"✅ Task deleted successfully: {task_id}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error deleting task: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False


def get_team_members(api_token, team_id):
    """
    Get team members for task assignment
    
    Args:
        api_token (str): ClickUp API token
        team_id (str): Team ID
    
    Returns:
        list: List of team members
    """
    headers = {
        "Authorization": api_token
    }
    
    url = f"https://api.clickup.com/api/v2/team/{team_id}/member"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        members = data.get('members', [])
        print(f"✅ Found {len(members)} team members")
        return members
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching team members: {e}")
        return []
