# Multi-Agent Task Management System

A comprehensive multi-agent system for task management, integrating Discord, ClickUp, and AI-powered analysis with a modern Streamlit dashboard.

## 🤖 Agents Overview

### Agent 1: Discord Integration
- Fetches messages from Discord channels
- Groups messages by user
- Summarizes conversations using AI models
- Outputs structured task data

### Agent 2: ClickUp Integration  
- Connects to ClickUp API for task management
- Organizes tasks by employee
- Generates comprehensive statistics
- Provides real-time task analytics

### Agent 3: AI Analysis
- Analyzes task completion patterns
- Categorizes work by status and deadlines
- Generates intelligent summaries
- Identifies missed deadlines and achievements

## 🚀 Features

- **Real-time Dashboard**: Modern Streamlit interface with live data visualization
- **Multi-Platform Integration**: Discord + ClickUp + AI analysis
- **SLM Support**: Efficient Small Language Model integration
- **Clean Architecture**: Modular design with separated concerns
- **Data Visualization**: Interactive charts and metrics
- **Version Control**: Full Git integration with GitHub

## 📁 Project Structure

```
├── Agent 1/                 # Discord integration
│   ├── discord_fetch.py     # Discord message fetching
│   ├── summary.py           # AI summarization
│   └── summary_slm.py       # SLM version
├── Agent 2/                 # ClickUp integration
│   ├── fetch_clickup.py     # ClickUp API client
│   ├── organize_tasks.py    # Task organization
│   └── agent2_main.py       # Main orchestration
├── Agent 3/                 # AI analysis
│   ├── finaly.py            # Task analysis
│   └── finaly_slm.py        # SLM version
├── dashboard.py             # Streamlit dashboard
├── sml_config.py           # SLM configuration
└── SLM_MIGRATION_GUIDE.md  # Migration documentation
```

## 🛠️ Setup

### Prerequisites
- Python 3.8+
- Discord Bot Token
- ClickUp API Token
- Required Python packages (see requirements.txt)

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure API tokens in respective agent files
4. Run individual agents or start the dashboard

### Quick Start
```bash
# Start the dashboard
python -m streamlit run dashboard.py --server.port 8501

# Run individual agents
python "Agent 1/summary.py"
python "Agent 2/agent2_main.py" 
python "Agent 3/finaly.py"
```

## 📊 Dashboard

Access the dashboard at `http://localhost:8501` to view:
- Real-time agent status
- ClickUp task analytics
- Discord message summaries
- AI-powered insights
- Interactive visualizations

## 🔧 Configuration

### API Tokens Required
- **Discord**: Bot token for message access
- **ClickUp**: API token for task management

### Environment Setup
- Configure tokens in respective agent files
- Set up ClickUp workspace (team, space, list)
- Ensure proper file permissions

## 📈 Features

- ✅ **Real-time Data**: Live updates from all agents
- ✅ **Interactive Charts**: Plotly-powered visualizations  
- ✅ **Multi-Platform**: Discord + ClickUp integration
- ✅ **AI Analysis**: Intelligent task categorization
- ✅ **Clean UI**: Modern Streamlit interface
- ✅ **Version Control**: Full Git integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- [GitHub Repository](https://github.com/amaan-1234/DevHacksS2)
- [ClickUp API Documentation](https://clickup.com/api)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

Built with ❤️ using Python, Streamlit, and modern AI technologies.
