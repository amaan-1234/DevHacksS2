# AZNN Multi‑Agent Dashboard — React Version

This is a React (Vite) port of your Streamlit dashboard. It reproduces the **three‑agent view**:
- **Agent 1 (Discord)**: loads `agent1_summary.json`
- **Agent 2 (ClickUp)**: loads `agent2_summary_clickup.json` and `agent2_clickup_statistics.json`, with charts + filters
- **Agent 3 (Analysis)**: loads `agent3_summary.json`
- **Task Management**: create/update/delete tasks *locally* for demo; optional Node proxy provided to wire real ClickUp

## 🧱 What’s inside
- React + Vite
- Recharts for charts
- Sample JSON in `public/data/` (copied from your AZNN repo)
- Optional `server/` Node proxy for ClickUp (avoids CORS and keeps your token server‑side)

## ▶️ Run the React app
```bash
# 1) Go to the project
cd aznn-react

# 2) Install deps
npm install

# 3) Start dev server
npm run dev
```
Then open the printed local URL (e.g., `http://localhost:5173`).  
The app reads sample data from `public/data` — no backend required.

## 🔌 (Optional) Wire real ClickUp
If you want the **Create/Update/Delete** in the UI to hit real ClickUp:
```bash
# in a separate terminal
cd aznn-react
cp .env.example .env
# edit .env and set CLICKUP_API_TOKEN=...
npm run server
```
This starts a small Express proxy at `http://localhost:4000`. You can point your frontend calls to it
(e.g., `/api/clickup/tasks`) to avoid CORS and keep tokens off the browser.

> **Note**: By default, the UI only updates **local state** (no persistence) to stay backend‑agnostic.
> If you need me to wire the frontend buttons to the proxy endpoints, I can add that too.

## 📁 Project tree
```
aznn-react
├── index.html
├── package.json
├── vite.config.js
├── .env.example
├── public
│   └── data
│       ├── agent1_summary.json
│       ├── agent2_summary_clickup.json
│       ├── agent2_clickup_statistics.json
│       └── agent3_summary.json
├── server
│   └── index.js
└── src
    ├── App.jsx
    ├── main.jsx
    └── components
        ├── AgentStatus.jsx
        ├── AnalysisSection.jsx
        ├── ClickUpSection.jsx
        └── DiscordSection.jsx
        └── TaskManagement.jsx
```

## 🧪 Differences vs Streamlit
- Plotly timeline is not included; if you’d like a Gantt timeline, I can add a lightweight React version.
- Task actions default to **local demo updates**. Use the proxy if you want ClickUp mutations.

## 🧼 No `process is not defined` pitfalls
This app uses Vite. No direct `process.env` usage in the browser code (use `import.meta.env` if needed).
