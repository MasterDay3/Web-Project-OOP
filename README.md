# 🔢 Numerix

**Numerix** is a web application for learning and working with historical numeral systems from around the world. Convert numbers, perform calculations, and train your knowledge through interactive tasks - all in one place.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔄 **Converter** | Convert numbers between Arabic, Roman, Egyptian, and Thai numeral systems |
| 🧮 **Calculator** | Perform arithmetic (+, −, ×, ÷, %, ^, √, !) directly in Roman, Egyptian, Thai, or Arabic numerals |
| 📚 **Tasks** | Multiple-choice training exercises with 4 difficulty levels |
| 📊 **Stats** | 30-day activity charts, accuracy graphs, and per-system breakdowns |
| 🏆 **Leaderboard** | Rankings by XP and daily streaks |
| 👤 **Profile** | Account settings, password change, daily goal configuration |
| ❌ **Mistakes** | Review and retry incorrectly answered tasks |

---

## 🌍 Supported Numeral Systems

- **Arabic** — standard 0–9 digits
- **Roman** — I, V, X, L, C, D, M (1–3999)
- **Egyptian** — hieroglyphic numerals ( 𓏺 𓎆 𓍢 𓆼 𓂭 𓆐 𓀼 )
- **Thai** — ๐ ๑ ๒ ๓ ๔ ๕ ๖ ๗ ๘ ๙
- **Binary** — base-2 (tasks only)

---

## 🐳 Running with Docker (Recommended)

Docker is the easiest way to run Numerix — no Python installation needed. It packages everything the app needs into one container that runs the same on any computer.

### Step 1 — Install Docker

If you don't have Docker yet:

- **Windows / macOS:** Download and install Docker Desktop — it's free. After installing, open the Docker Desktop app and wait for it to start (you'll see the whale icon in your taskbar/menu bar turn steady).
- **Linux:** Follow the official install guide for your distro.

### Step 2 — Get the project files

Download or clone this repository and open a terminal inside the project folder:
```bash
cd path/to/numerix
```

### Step 3 — Build the app

This command reads the project files and prepares the app. You only need to do this once (and again if you update the code):
```bash
docker build -t numerix .
```

### Step 4 — Launch the app

Make the launch script executable (one time only):
```bash
chmod +x start.sh
```

Then start the app any time with:
```bash
./start.sh
```

Your browser will open automatically at **http://localhost:5000** 🎉

### Stopping the app

```bash
docker stop numerix_app && docker rm numerix_app
```

Or just run `./start.sh` again next time — it cleans up automatically.

---

## 🚀 Running Locally

Use this method if you prefer not to use Docker and have Python installed.

### Prerequisites

- Python **3.10+**
- pip

### 1. Clone the repository

```bash
git clone https://github.com/your-username/numerix.git
cd numerix
```

### 2. Create and activate a virtual environment

#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```
---
#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

The app will start at **http://127.0.0.1:5000**

---

## 🗂️ Project Structure

```
numerix/
├── app.py                  # Main Flask application & routes
├── models.py               # SQLAlchemy database models
├── numsystems.py           # Convertor and Calculator classes
├── tasks.py                # Task generator (multiple-choice)
├── requirements.txt        # Python dependencies
├── Dockerfile
│
├── routes/
│   ├── auth_routes.py      # Login, register, logout
│   ├── task_routes.py      # Task generation and answer submission
│   ├── profile_routes.py   # User profile management
│   ├── leaderboard_routes.py
│   ├── stats_routes.py
│   └── mistakes_routes.py
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html          # Converter page
│   ├── calculator.html
│   ├── tasks.html
│   ├── dashboard.html
│   ├── stats.html
│   ├── leaderboard.html
│   ├── mistakes.html
│   ├── profile.html
│   ├── login.html
│   └── register.html
│
├── static/
│   ├── css/style.css
│   └── js/main.js
│
└── tasks/
    ├── roman_math_tasks.csv
    ├── egyptian_math_tasks.csv
    └── thai_math_tasks.csv
```

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask-Login, Flask-SQLAlchemy, Flask-Migrate
- **Database:** SQLite (default) / PostgreSQL (production)
- **Frontend:** Vanilla HTML, CSS, JavaScript (no frameworks)
- **Charts:** Chart.js

---

## 👥 Authors

Mykola Zabulskyi - Backend Core (Auth + Users + API)

Yurii Melnyk - Frontend (HTML + CSS + interactions)

Maryan Dmytriv - Backend Logic (Numbers Engine)

Uliana Kryshchuk - Product / QA / Architect
