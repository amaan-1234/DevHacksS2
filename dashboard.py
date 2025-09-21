import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add Agent 2 directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'Agent 2'))

# Import ClickUp functions
try:
    from fetch_clickup import (
        fetch_tasks_from_clickup, 
        create_task_in_clickup, 
        update_task_in_clickup, 
        delete_task_in_clickup,
        get_team_members,
        get_team_info,
        get_spaces_from_team,
        get_lists_from_space
    )
    from clickup_config import CLICKUP_API_TOKEN, DEFAULT_PRIORITY, DEFAULT_STATUS
    CLICKUP_AVAILABLE = True
except ImportError as e:
    st.warning(f"⚠️ ClickUp integration not available: {e}")
    CLICKUP_AVAILABLE = False

# --- Load and parse data ---
try:
    with open("Agent 1/summary.json") as f1:
        raw_tasks = json.load(f1)
    summary_df = pd.DataFrame(raw_tasks)
    st.success(f"✅ Agent 1: Loaded {len(summary_df)} tasks")
except FileNotFoundError:
    st.warning("⚠️ Agent 1 data not found. Using sample data.")
    summary_df = pd.DataFrame([])
except Exception as e:
    st.error(f"❌ Agent 1 error: {str(e)}")
    summary_df = pd.DataFrame([])

try:
    with open("Agent 2/summary_clickup.json") as f2:
        clickup_tasks = json.load(f2)
    
    with open("Agent 2/clickup_statistics.json") as f2_stats:
        clickup_stats = json.load(f2_stats)
    
    # Convert ClickUp data to DataFrame
    clickup_data = []
    for employee, tasks in clickup_tasks.items():
        for task in tasks:
            task['employee'] = employee
            clickup_data.append(task)
    
    clickup_df = pd.DataFrame(clickup_data)
    
    # Convert ClickUp dates
    if not clickup_df.empty:
        clickup_df["date_created"] = pd.to_datetime(clickup_df["date_created"], unit='ms', errors="coerce")
        clickup_df["date_updated"] = pd.to_datetime(clickup_df["date_updated"], unit='ms', errors="coerce")
        clickup_df["due_date"] = pd.to_datetime(clickup_df["due_date"], errors="coerce")
        clickup_df["date_closed"] = pd.to_datetime(clickup_df["date_closed"], unit='ms', errors="coerce")
    
    st.success(f"✅ Agent 2: Loaded {len(clickup_df)} ClickUp tasks")
except FileNotFoundError:
    st.warning("⚠️ Agent 2 ClickUp data not found. Using sample data.")
    clickup_df = pd.DataFrame([])
    clickup_stats = {"total_employees": 0, "total_tasks": 0, "employee_stats": {}}
except Exception as e:
    st.error(f"❌ Agent 2 error: {str(e)}")
    clickup_df = pd.DataFrame([])
    clickup_stats = {"total_employees": 0, "total_tasks": 0, "employee_stats": {}}

try:
    with open("Agent 3/summary.json") as f3:  
        text_summary = json.load(f3)
    st.success(f"✅ Agent 3: Loaded analysis data with {len(text_summary)} categories")
except FileNotFoundError:
    st.warning("⚠️ Agent 3 data not found. Using sample data.")
    text_summary = {"Work completed": [], "Work not completed": [], "Tasks completed on time": [], "Missed deadlines": []}
except Exception as e:
    st.error(f"❌ Agent 3 error: {str(e)}")
    text_summary = {"Work completed": [], "Work not completed": [], "Tasks completed on time": [], "Missed deadlines": []}


# Convert dates
if not summary_df.empty:
    summary_df["deadline"] = pd.to_datetime(summary_df["deadline"], errors="coerce")
    summary_df["completed_date"] = pd.to_datetime(summary_df["completed_date"], errors="coerce")

# --- ClickUp Task Management Functions ---
def load_clickup_config():
    """Load ClickUp configuration from config.json"""
    try:
        with open("Agent 2/config.json", "r") as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("❌ ClickUp config.json not found")
        return None
    except Exception as e:
        print(f"❌ Error loading ClickUp config: {e}")
        return None

@st.cache_data(ttl=60)  # Cache for 60 seconds
def refresh_clickup_data():
    """Refresh ClickUp data by fetching from API"""
    if not CLICKUP_AVAILABLE:
        return None, None
    
    config = load_clickup_config()
    if not config or not config.get("list_id"):
        return None, None
    
    try:
        # Fetch fresh data from ClickUp
        tasks = fetch_tasks_from_clickup(
            api_token=config["api_token"],
            list_id=config["list_id"]
        )
        
        if not tasks:
            return None, None
        
        # Organize tasks by employee
        from organize_tasks import organize_tasks_by_employee, get_task_statistics, save_organized_tasks, save_task_statistics
        
        organized_tasks = organize_tasks_by_employee(tasks)
        stats = get_task_statistics(organized_tasks)
        
        # Save updated data
        save_organized_tasks(organized_tasks, "Agent 2/summary_clickup.json")
        save_task_statistics(stats, "Agent 2/clickup_statistics.json")
        
        # Convert to DataFrame
        clickup_data = []
        for employee, emp_tasks in organized_tasks.items():
            for task in emp_tasks:
                task['employee'] = employee
                clickup_data.append(task)
        
        clickup_df = pd.DataFrame(clickup_data)
        
        # Convert dates
        if not clickup_df.empty:
            clickup_df["date_created"] = pd.to_datetime(clickup_df["date_created"], unit='ms', errors="coerce")
            clickup_df["date_updated"] = pd.to_datetime(clickup_df["date_updated"], unit='ms', errors="coerce")
            clickup_df["due_date"] = pd.to_datetime(clickup_df["due_date"], errors="coerce")
            clickup_df["date_closed"] = pd.to_datetime(clickup_df["date_closed"], unit='ms', errors="coerce")
        
        return clickup_df, stats
        
    except Exception as e:
        st.error(f"❌ Error refreshing ClickUp data: {e}")
        return None, None

def create_new_task(task_name, description, assignee, priority, due_date, status):
    """Create a new task in ClickUp"""
    if not CLICKUP_AVAILABLE:
        st.error("❌ ClickUp integration not available")
        return False
    
    config = load_clickup_config()
    if not config or not config.get("list_id"):
        st.error("❌ ClickUp configuration not found. Please run Agent 2 first to set up ClickUp.")
        return False
    
    # Prepare task data according to ClickUp API format
    task_data = {
        "name": task_name,
        "description": description or "",
        "notify_all": True
    }
    
    # Add status if provided
    if status:
        task_data["status"] = status
    
    # Add priority if provided (ClickUp expects specific values)
    priority_mapping = {
        "Urgent": 4,
        "High": 3, 
        "Normal": 2,
        "Low": 1
    }
    if priority and priority in priority_mapping:
        task_data["priority"] = priority_mapping[priority]
    
    # Add assignee if provided (ClickUp expects user IDs, not usernames)
    if assignee and assignee != "Unassigned":
        # For now, we'll skip assignee assignment as it requires user ID lookup
        st.info(f"ℹ️ Assignee '{assignee}' will be set as unassigned (requires user ID lookup)")
    
    # Add due date if provided
    if due_date:
        try:
            # Convert date to datetime and then to timestamp
            due_datetime = datetime.combine(due_date, datetime.min.time())
            task_data["due_date"] = int(due_datetime.timestamp() * 1000)
        except Exception as e:
            st.warning(f"⚠️ Could not set due date: {e}")
    
    try:
        # Debug information
        st.info(f"🔍 Creating task with config: API token starts with {config['api_token'][:10]}..., List ID: {config['list_id']}")
        st.info(f"🔍 Task data: {task_data}")
        
        result = create_task_in_clickup(
            api_token=config["api_token"],
            list_id=config["list_id"],
            task_data=task_data
        )
        
        if result:
            st.success(f"✅ Task '{task_name}' created successfully!")
            # Clear cache to force refresh
            refresh_clickup_data.clear()
            return True
        else:
            st.error("❌ Failed to create task. Check your ClickUp API token and permissions.")
            return False
            
    except Exception as e:
        st.error(f"❌ Error creating task: {e}")
        return False

def update_task_status(task_id, new_status):
    """Update task status in ClickUp"""
    if not CLICKUP_AVAILABLE:
        return False
    
    config = load_clickup_config()
    if not config:
        return False
    
    # ClickUp requires status to be updated using the status ID, not the status name
    # We need to map status names to status IDs
    status_mapping = {
        "to do": "to do",
        "in progress": "in progress", 
        "complete": "complete",
        "closed": "closed"
    }
    
    task_data = {"status": status_mapping.get(new_status, new_status)}
    
    try:
        result = update_task_in_clickup(
            api_token=config["api_token"],
            task_id=task_id,
            task_data=task_data
        )
        if result is not None:
            # Clear cache to force refresh
            refresh_clickup_data.clear()
        return result is not None
    except Exception as e:
        st.error(f"❌ Error updating task: {e}")
        return False


# --- Streamlit Layout ---
st.set_page_config(page_title="Multi-Agent Task Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center;'>🤖 Multi-Agent Task Management Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Agent Status Overview ---
st.markdown("## 🔄 Agent Status")
col1, col2, col3, col4 = st.columns(4)

# Agent 1 Status
agent1_status = "✅ Active" if not summary_df.empty else "⚠️ No Data"
col1.metric("Agent 1 (Discord)", agent1_status, len(summary_df))

# Agent 2 Status  
agent2_status = "✅ Active" if not clickup_df.empty else "⚠️ No Data"
col2.metric("Agent 2 (ClickUp)", agent2_status, len(clickup_df))

# Agent 3 Status
agent3_status = "✅ Active" if text_summary else "⚠️ No Data"
col3.metric("Agent 3 (Analysis)", agent3_status, "Ready")

# Overall Status
total_tasks = len(summary_df) + len(clickup_df)
col4.metric("Total Tasks", total_tasks, "Across All Agents")

st.markdown("---")

# --- ClickUp Metrics ---
if not clickup_df.empty:
    st.markdown("## 📊 ClickUp Task Analytics")
    
    # ClickUp specific metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Task status breakdown
    status_counts = clickup_df['status'].value_counts()
    completed_clickup = len(clickup_df[clickup_df['status'].isin(['complete', 'done', 'closed'])])
    in_progress_clickup = len(clickup_df[clickup_df['status'] == 'in progress'])
    todo_clickup = len(clickup_df[clickup_df['status'] == 'to do'])
    
    col1.metric("✅ Completed", completed_clickup)
    col2.metric("🔄 In Progress", in_progress_clickup)
    col3.metric("📋 To Do", todo_clickup)
    col4.metric("👥 Employees", clickup_stats.get('total_employees', 0))
    
    # Employee performance
    if clickup_stats.get('employee_stats'):
        st.markdown("### 👥 Employee Performance")
        emp_cols = st.columns(len(clickup_stats['employee_stats']))
        for i, (emp, stats) in enumerate(clickup_stats['employee_stats'].items()):
            with emp_cols[i]:
                st.metric(
                    f"👤 {emp}",
                    f"{stats['completed_tasks']}/{stats['total_tasks']}",
                    f"{stats['completion_rate']}%"
                )
    
    st.markdown("---")

# --- Task Management Section ---
if CLICKUP_AVAILABLE:
    st.markdown("## 🛠️ Task Management")
    
    # Create two columns for task creation and management
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ➕ Create New Task")
        
        with st.form("create_task_form"):
            task_name = st.text_input("Task Name", placeholder="Enter task name...")
            task_description = st.text_area("Description", placeholder="Enter task description...")
            
            # Get team members for assignment
            config = load_clickup_config()
            assignee_options = ["Unassigned"]
            if config and config.get("team_id"):
                try:
                    members = get_team_members(config["api_token"], config["team_id"])
                    assignee_options.extend([member.get("user", {}).get("username", "Unknown") for member in members])
                except:
                    pass
            
            assignee = st.selectbox("Assign to", assignee_options)
            priority = st.selectbox("Priority", ["Urgent", "High", "Normal", "Low"], index=2)
            due_date = st.date_input("Due Date", value=datetime.now().date() + timedelta(days=7))
            status = st.selectbox("Status", ["to do", "in progress", "complete"], index=0)
            
            submitted = st.form_submit_button("🚀 Create Task", type="primary")
            
            if submitted:
                if task_name:
                    success = create_new_task(
                        task_name=task_name,
                        description=task_description,
                        assignee=assignee if assignee != "Unassigned" else None,
                        priority=priority,
                        due_date=due_date,
                        status=status
                    )
                    if success:
                        st.rerun()  # Refresh the page to show new task
                else:
                    st.error("❌ Please enter a task name")
    
    with col2:
        st.markdown("### 🔄 Task Actions")
        
        # Refresh data button
        if st.button("🔄 Refresh from ClickUp", type="secondary"):
            with st.spinner("Refreshing data from ClickUp..."):
                new_clickup_df, new_clickup_stats = refresh_clickup_data()
                if new_clickup_df is not None:
                    clickup_df = new_clickup_df
                    clickup_stats = new_clickup_stats
                    st.success("✅ Data refreshed successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to refresh data")
        
        # Test API connection button
        if st.button("🧪 Test API Connection", type="secondary"):
            config = load_clickup_config()
            if config:
                try:
                    # Test with a simple API call
                    from fetch_clickup import get_team_info
                    teams = get_team_info(config["api_token"])
                    if teams:
                        st.success(f"✅ API connection successful! Found {len(teams)} teams.")
                    else:
                        st.error("❌ API connection failed - no teams found")
                except Exception as e:
                    st.error(f"❌ API connection failed: {e}")
            else:
                st.error("❌ No ClickUp configuration found")
        
        # Quick status update
        if not clickup_df.empty:
            st.markdown("#### 📝 Quick Status Update")
            
            # Get tasks for status update
            task_options = clickup_df[['id', 'name', 'status']].copy()
            task_options['display'] = task_options['name'] + " (" + task_options['status'] + ")"
            
            selected_task = st.selectbox(
                "Select Task", 
                options=task_options.index,
                format_func=lambda x: task_options.loc[x, 'display']
            )
            
            current_status = task_options.loc[selected_task, 'status']
            status_options = ["to do", "in progress", "complete", "closed"]
            try:
                current_index = status_options.index(current_status)
            except ValueError:
                current_index = 0
            
            new_status = st.selectbox(
                "New Status",
                status_options,
                index=current_index
            )
            
            if st.button("📝 Update Status"):
                task_id = task_options.loc[selected_task, 'id']
                if update_task_status(task_id, new_status):
                    st.success("✅ Status updated successfully!")
                    # Force refresh the data
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error("❌ Failed to update status")

st.markdown("---")

# --- Tabs for detailed views ---
tab1, tab2, tab3 = st.tabs(["📊 ClickUp Tasks", "🧾 Discord Tasks", "📄 Text Summary"])

with tab1:
    if not clickup_df.empty:
        st.subheader("📋 ClickUp Task Overview")
        
        # Task status distribution
        if 'status' in clickup_df.columns:
            status_fig = px.pie(clickup_df, names='status', title="Task Status Distribution")
            st.plotly_chart(status_fig, use_container_width=True)
        
        # Employee task breakdown
        if 'employee' in clickup_df.columns:
            emp_fig = px.bar(clickup_df['employee'].value_counts().reset_index(), 
                           x='employee', y='count', 
                           title="Tasks by Employee")
            st.plotly_chart(emp_fig, use_container_width=True)
        
        # Interactive task management
        st.subheader("📋 All ClickUp Tasks")
        
        # Add filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All"] + list(clickup_df['status'].unique()))
        with col2:
            priority_filter = st.selectbox("Filter by Priority", ["All"] + list(clickup_df['priority'].unique()))
        with col3:
            employee_filter = st.selectbox("Filter by Employee", ["All"] + list(clickup_df['employee'].unique()))
        
        # Apply filters
        filtered_df = clickup_df.copy()
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        if priority_filter != "All":
            filtered_df = filtered_df[filtered_df['priority'] == priority_filter]
        if employee_filter != "All":
            filtered_df = filtered_df[filtered_df['employee'] == employee_filter]
        
        # Display filtered tasks
        display_cols = ['name', 'status', 'priority', 'employee', 'creator', 'date_created', 'url']
        available_cols = [col for col in display_cols if col in filtered_df.columns]
        
        # Add action buttons for each task
        if not filtered_df.empty:
            for idx, task in filtered_df.iterrows():
                with st.expander(f"📝 {task.get('name', 'Untitled')} - {task.get('status', 'Unknown')}"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**Description:** {task.get('description', 'No description')}")
                        st.write(f"**Priority:** {task.get('priority', 'Normal')}")
                        st.write(f"**Assignee:** {task.get('employee', 'Unassigned')}")
                        if task.get('due_date'):
                            st.write(f"**Due Date:** {task.get('due_date')}")
                        if task.get('url'):
                            st.write(f"**ClickUp Link:** [Open in ClickUp]({task.get('url')})")
                    
                    with col2:
                        if st.button(f"✅ Complete", key=f"complete_{task.get('id', idx)}"):
                            if update_task_status(task.get('id'), 'complete'):
                                st.success("Task completed!")
                                # Force refresh the data
                                st.cache_data.clear()
                                st.rerun()
                    
                    with col3:
                        if st.button(f"🔄 In Progress", key=f"progress_{task.get('id', idx)}"):
                            if update_task_status(task.get('id'), 'in progress'):
                                st.success("Status updated!")
                                # Force refresh the data
                                st.cache_data.clear()
                                st.rerun()
        
        # Summary table
        st.subheader("📊 Task Summary")
        st.dataframe(filtered_df[available_cols], use_container_width=True)
        
        # Task details by status
        for status in clickup_df['status'].unique():
            if pd.notna(status):
                st.subheader(f"📋 {status.title()} Tasks")
                status_tasks = clickup_df[clickup_df['status'] == status]
                st.dataframe(status_tasks[available_cols], use_container_width=True)
    else:
        st.info("No ClickUp data available. Run Agent 2 to fetch tasks.")

with tab2:
    if not summary_df.empty:
        st.subheader("📋 Discord Task Overview")
        
        # Task status distribution for Discord tasks
        if 'status' in summary_df.columns:
            discord_status_fig = px.pie(summary_df, names='status', title="Discord Task Status Distribution")
            st.plotly_chart(discord_status_fig, use_container_width=True)
        
        st.subheader("✅ Completed Tasks")
        completed_tasks = summary_df[summary_df.status == "completed"]
        if not completed_tasks.empty:
            st.dataframe(completed_tasks, use_container_width=True)
        else:
            st.info("No completed tasks found.")

        st.subheader("❌ Incomplete Tasks")
        incomplete_tasks = summary_df[summary_df.status == "not completed"]
        if not incomplete_tasks.empty:
            st.dataframe(incomplete_tasks, use_container_width=True)
        else:
            st.info("No incomplete tasks found.")
    else:
        st.info("No Discord task data available. Run Agent 1 to fetch Discord messages.")

with tab3:
    st.subheader("📘 Work Completed")
    for item in text_summary["Work completed"]:
        st.success(f"✔️ {item}")
    st.subheader("⚠️ Work Not Completed")
    for item in text_summary["Work not completed"]:
        st.warning(f"❌ {item}")
    st.subheader("📅 Tasks Completed On Time")
    for item in text_summary["Tasks completed on time"]:
        st.info(f"🕒 {item}")
    if text_summary["Missed deadlines"]:
        st.subheader("🚨 Missed Deadlines")
        for item in text_summary["Missed deadlines"]:
            st.error(f"⏰ {item}")
    else:
        st.info("✅ No missed deadlines!")

# --- Timeline and Charts ---
st.markdown("## 📊 Task Analytics & Timeline")

# Real-time refresh button
if st.button("🔄 Refresh Data", type="primary"):
    st.rerun()

# ClickUp timeline if available
if not clickup_df.empty and 'date_created' in clickup_df.columns:
    st.markdown("### 📅 ClickUp Task Timeline")
    clickup_timeline = clickup_df.copy()
    clickup_timeline["Task"] = clickup_timeline["name"]
    clickup_timeline["Start"] = clickup_timeline["date_created"]
    clickup_timeline["End"] = clickup_timeline["due_date"].fillna(clickup_timeline["date_updated"])
    
    # Filter out invalid dates
    clickup_timeline = clickup_timeline.dropna(subset=['Start'])
    
    if not clickup_timeline.empty:
        fig_clickup = px.timeline(clickup_timeline, x_start="Start", x_end="End", y="Task", 
                                color="status", title="ClickUp Task Timeline")
        fig_clickup.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_clickup, use_container_width=True)

# Discord timeline
if not summary_df.empty:
    st.markdown("### 📅 Discord Task Timeline")
    timeline_df = summary_df.copy()
    timeline_df["Task"] = timeline_df["description"]
    timeline_df["Start"] = timeline_df["completed_date"].fillna(timeline_df["deadline"])
    timeline_df["End"] = timeline_df["deadline"]

    fig = px.timeline(timeline_df, x_start="Start", x_end="End", y="Task", color="status", title="Discord Task Timeline")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

# Agent execution status
st.markdown("## 🤖 Agent Execution Status")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Agent 1 (Discord)")
    if not summary_df.empty:
        st.success("✅ Data Available")
        st.write(f"Tasks: {len(summary_df)}")
    else:
        st.warning("⚠️ No Data")

with col2:
    st.markdown("### Agent 2 (ClickUp)")
    if not clickup_df.empty:
        st.success("✅ Data Available")
        st.write(f"Tasks: {len(clickup_df)}")
        st.write(f"Employees: {clickup_stats.get('total_employees', 0)}")
    else:
        st.warning("⚠️ No Data")

with col3:
    st.markdown("### Agent 3 (Analysis)")
    if text_summary and any(text_summary.values()):
        st.success("✅ Analysis Complete")
    else:
        st.warning("⚠️ No Analysis")

st.markdown("---")
st.caption("🔧 Built with Streamlit · 🤖 Multi-Agent System · 📊 Real-time ClickUp Integration · 💡 Dashboard Summary View")
