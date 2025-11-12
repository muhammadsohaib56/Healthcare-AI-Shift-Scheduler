# **Inovaqo AI Scheduling Assistant**  
**Healthcare Staff Management System with Natural Language AI**

---

*AI-Powered Shift Management for Hospitals & Clinics*

---

## Overview

**Inovaqo AI Scheduling Assistant** is a full-stack, AI-powered web application designed to streamline **staff scheduling** in healthcare facilities. Using **natural language processing (NLP)**, staff can **call off**, **reactivate**, or **update shift times** simply by sending a message — no forms, no logins, no hassle.

Built with **FastAPI (Python)**, **React (TypeScript)**, **SQLAlchemy**, and **LangChain**, this system enables real-time, intelligent schedule management with **zero false matches** and **professional-grade UI**.

---

## Key Features

| Feature | Description |
|--------|-----------|
| **Natural Language Interface** | Staff say: *"I can't take my 9 AM shift"* → AI updates instantly |
| **Call Off & Reactivate** | `I'm sick` → Called Off<br>`I'm available again` → Active |
| **Update Shift Time** | `I'm available from 10:00 to 18:00` → Time updated |
| **Exact Name Matching** | `Dr. Ahmed` ≠ `Nurse Ahmed` — no mix-ups |
| **Greeting Support** | `Hello`, `Good morning` → Friendly AI response |
| **Real-Time Sync** | Schedule auto-refreshes every 5 seconds |
| **Professional UI** | Hospital-grade design with stats, avatars, and responsive layout |
| **Persistent Storage** | SQLite + SQLAlchemy (easy to upgrade to PostgreSQL) |
| **CORS & Security** | Production-ready backend with CORS middleware |

---

## Tech Stack

### Backend
- **FastAPI** – High-performance Python web framework
- **SQLAlchemy** – ORM for database operations
- **SQLite** – Lightweight, file-based database (dev/prod-ready)
- **LangChain** – AI orchestration
- **OpenRouter API** – LLM backend (openai/GPT-oss-120b / open-source models)
- **Pydantic** – Structured AI output validation

### Frontend
- **React 18** – Component-based UI
- **Tailwind CSS** – Utility-first styling
- **date-fns** – Clean date/time formatting
- **Axios** – API client
- **Vite** – Fast build tool

---

## Project Structure

```
scheduling-assistant/
│
├── .gitignore
├── README.md                     (Optional – add for pro look)
│
├── backend/
│   ├── .env                      (IGNORED – not in Git)
│   ├── schedule.db               (IGNORED – not in Git)
│   ├── requirements.txt
│   │
│   ├── app/
│   │   ├── __init__.py           (empty or not needed)
│   │   ├── main.py
│   │   ├── database.py
│   │   └── config.py
│   │
│   └── healthcare_assistant/
│       ├── __init__.py           (empty or not needed)
│       ├── router.py
│       ├── service.py
│       ├── repository.py
│       ├── models.py             (SQLAlchemy + Pydantic Schema)
│       ├── agent.py
│       └── prompts.py
│
└── frontend/
    ├── .env                      (IGNORED – not in Git)
    ├── package.json
    ├── package-lock.json
    ├── postcss.config.js
    ├── tailwind.config.js
    │
    ├── public/
    │   └── index.html
    │
    └── src/
        ├── index.js
        ├── index.css
        ├── api.js
        ├── App.jsx
        │
        └── components/
            ├── ChatBox.jsx       (unused – kept for reference)
            ├── MessageBubble.jsx (unused – kept for reference)
            └── ScheduleTable.jsx (UPDATED: scroll after 6 rows)
```

---

## How It Works

1. **Staff opens the web app** → Sees current week’s schedule
2. **Types a message** → e.g., `I can't take my 9 AM shift`
3. **AI (LangChain + OpenRouter)** analyzes:
   - Intent: `call_off`
   - Exact provider: `Dr. Ahmed`
   - Shift ID: `1`
4. **Backend updates DB** → `status = "called_off"`
5. **Frontend auto-refreshes** → Shows **Called Off** in red
6. **Reverse actions** supported: `I'm available again`, `Update to 10:00-18:00`

---

## AI Intent Detection

| User Input | Intent | Action |
|----------|--------|-------|
| `I can't come` | `call_off` | Mark shift as Called Off |
| `I'm available again` | `reactivate` | Restore to Active |
| `I'm free from 10:00 to 18:00` | `update_shift_time` | Update time |
| `Hello` | `greeting` | Friendly reply |
| `Who is on tomorrow?` | `query` | Return schedule info |

> **Exact name matching** ensures zero errors.

---

## Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/muhammadsohaib56/inovaqo-scheduling-assistant.git
cd inovaqo-scheduling-assistant
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Create `.env` in `backend/`
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=openai/gpt-oss-120b
DATABASE_URL=sqlite:///schedule.db
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

### 4. Run the Application

#### Terminal 1 – Backend
```bash
cd backend
uvicorn app.main:app --reload --port=8000
```

#### Terminal 2 – Frontend
```bash
cd frontend
npm run dev
```

Open: [http://localhost:5173](http://localhost:5173)

---

## Sample Data (Auto-Seeded)

| Provider | Date | Time | Status |
|--------|------|------|--------|
| Dr. Ahmed | Nov 12 | 09:00 – 17:00 | Active |
| Nurse Sara | Nov 13 | 14:00 – 22:00 | Active |
| Dr. Khan | Nov 14 | 08:00 – 16:00 | Active |
| Dr. Fatima | Nov 12 | 10:00 – 18:00 | Active |
| Nurse Ali | Nov 13 | 08:00 – 16:00 | Active |
| Dr. Zain | Nov 14 | 14:00 – 22:00 | Active |

---

## API Endpoints

| Method | Endpoint | Description |
|-------|---------|-----------|
| `GET` | `/api/schedule` | Get all shifts |
| `POST` | `/api/chat` | Send message to AI |

---

## Contributing

1. Fork the repo
2. Create a feature branch
3. Commit changes
4. Push and open a Pull Request

---

## Made with Love in Pakistan  
**November 11, 2025**

---

**Inovaqo AI Scheduler** – *Where AI meets real-world healthcare.*

---

**Star this project if you found it helpful!**

--- 
