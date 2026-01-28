# AI Assistant Manipur – Farmer Advisory System

This repository contains the prototype of an AI‑based Farmer Advisory System developed for the Imphal region of Manipur.  
The system has a frontend web interface and a backend AI API that provides agriculture‑related advisories.

---

## Project Structure

## Project Structure

```text
AI_Assistant_Manipur/
├── backend/
│   ├── api.py
│   ├── query.py
│   ├── ingest.py
│   ├── requirements.txt
│   ├── data/
│   │   └── documents/        # Government PDFs
│   ├── chroma_db/            # Vector database (auto-generated)
│   └── venv/                 # Python virtual environment
│
├── frontend/
│   ├── index.html
│   ├── ai-assistant.html
│   ├── advisory.html
│   ├── schemes.html
│   ├── app.js
│   ├── style.css
│   └── assets/
│
└── README.md


## Run Instructions

Step 1: Activate virtual environment
source venv/bin/activate
(Windows users: venv\Scripts\activate)

Step 2: Install dependencies
pip install -r requirements.txt

Step 3: Ingest documents (run once)
python ingest.py

Step 4: Start backend server
uvicorn api:app --reload
Backend will run at:
http://127.0.0.1:8000

Frontend Setup
Step 1: Navigate to frontend folder
cd ../frontend

Step 2: Open the website
Open index.html directly in a browser
OR
Use a simple server:
python -m http.server 5500

Then open:
http://localhost:5500/index.html
