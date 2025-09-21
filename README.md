# Multi-Agent Task Management System

A comprehensive multi-agent system for task management, integrating Discord, ClickUp, and AI-powered analysis with both Streamlit and React dashboards.

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

- **Dual Dashboard Support**: Both Streamlit and React interfaces
- **Real-time Data**: Live updates from all agents
- **Multi-Platform Integration**: Discord + ClickUp + AI analysis
- **Team Workload Equalizer**: Visual workload distribution and balancing
- **Interactive Charts**: Plotly-powered visualizations (Streamlit) and Recharts (React)
- **Clean Architecture**: Modular design with separated concerns
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
├── SLM_MIGRATION_GUIDE.md  # Migration documentation
├── server/                 # React app backend
│   └── index.js            # ClickUp API proxy
├── src/                    # React app frontend
│   ├── App.jsx
│   ├── main.jsx
│   └── components/
│       ├── ClickUpSection.jsx
│       ├── TaskManagement.jsx
│       └── TeamLoadEqualizer.jsx
├── public/data/            # Sample data files
└── package.json            # React dependencies
```

## 🛠️ Setup

### Prerequisites
- Python 3.8+ (for Streamlit version)
- Node.js 16+ (for React version)
- Discord Bot Token
- ClickUp API Token

### Streamlit Dashboard Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure API tokens in respective agent files

3. Run the Streamlit dashboard:
```bash
python -m streamlit run dashboard.py --server.port 8501
```

4. Access at `http://localhost:8501`

### React Dashboard Setup

1. Install Node.js dependencies:
```bash
npm install
```

2. Start the React development server:
```bash
npm run dev
```

3. Access at `http://localhost:5173`

4. (Optional) Start ClickUp API proxy:
```bash
# Create .env file with your ClickUp API token
cp .env.example .env
# Edit .env and add: CLICKUP_API_TOKEN=your_token_here

# Start the proxy server
npm run server
```

## 📊 Dashboard Features

### Streamlit Dashboard (`http://localhost:8501`)
- Real-time agent status
- ClickUp task analytics
- Discord message summaries
- AI-powered insights
- Interactive visualizations
- Team workload equalizer

### React Dashboard (`http://localhost:5173`)
- Modern React interface
- ClickUp task management
- Team workload equalizer with visual bars
- Real-time task creation/updates
- ClickUp API integration
- Responsive design

## 🔧 Configuration

### API Tokens Required
- **Discord**: Bot token for message access
- **ClickUp**: API token for task management

### Environment Setup
- Configure tokens in respective agent files
- Set up ClickUp workspace (team, space, list)
- Ensure proper file permissions

## 📈 Key Features

- ✅ **Real-time Data**: Live updates from all agents
- ✅ **Interactive Charts**: Plotly (Streamlit) and Recharts (React)
- ✅ **Multi-Platform**: Discord + ClickUp integration
- ✅ **AI Analysis**: Intelligent task categorization
- ✅ **Team Workload Equalizer**: Visual workload distribution
- ✅ **Dual Interface**: Both Streamlit and React dashboards
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
- [React Documentation](https://reactjs.org/)
- [Vite Documentation](https://vitejs.dev/)

---

Built with ❤️ using Python, Streamlit, React, and modern AI technologies.