# 🌿 Suwa Sahaya — සුව සහාය
**Free Healthcare AI for Sri Lanka — Powered by Claude (Anthropic)**

---

## ගොනු (Files)
```
project/
├── app.py                    ← Python backend server
├── index.html                ← Frontend web app
├── hospitals.csv             ← 50 government hospitals
├── medicine_alternatives.csv ← 50 medicine alternatives
├── symptoms_conditions.csv   ← 50 symptom profiles
├── volunteer_doctors.csv     ← 50 volunteer doctors
├── requirements.txt
└── README.md
```

---

## ✅ Setup (Setup කරන්නේ කෙසේද)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Anthropic API key set කරන්න
**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```
**Mac / Linux:**
```bash
export ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```
> API key ලබාගන්නේ: https://console.anthropic.com

### 3. Server start කරන්න
```bash
python app.py
```

### 4. Browser open කරන්න
```
http://localhost:5000
```

---

## 🔧 How It Works

1. `app.py` starts and **loads all 4 CSV files** into memory
2. CSV data is **injected into Claude's system prompt** — so Claude knows all hospitals, doctors, medicines
3. When user sends a chat message, the frontend calls `/api/chat`  
4. Python sends the message to **Anthropic Claude API** with full dataset context
5. Claude responds accurately using the real Sri Lankan healthcare data
6. Response is shown in the chat UI

---

## 📡 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/chat` | Main chat endpoint — sends to Claude with CSV context |
| `GET /api/doctors?district=colombo&spec=cardiologist` | Filter doctors |
| `GET /api/hospitals?district=galle` | Filter hospitals |
| `GET /api/medicines?q=panadol` | Search medicines |

---

## 🆘 Emergency Numbers
- **1990** — Suwa Seriya Ambulance
- **1979** — Health Information Hotline  
- **1926** — Mental Health Support
