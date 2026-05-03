# 🌿 Suwa Sahaya — සුව සහාය

> **Free Healthcare AI for Sri Lanka** | AI-powered health assistant with hospital directory, medicine alternatives, symptom checker, and volunteer doctor network.

---

## ✨ Features

- 🤖 **AI Health Assistant** — Chat in English or Sinhala, powered by Groq LLM (llama, mixtral, gemma models)
- 💊 **Medicine Alternatives** — Find affordable generic medicines with price comparisons and free government hospital availability
- 🏥 **Hospital Directory** — Search hospitals by district with emergency contacts and services
- 🩺 **Volunteer Doctor Network** — Connect with volunteer doctors by specialization and district
- 🔍 **Symptom Checker** — Get urgency levels, home remedies, and guidance on when to see a doctor
- 🌐 **Bilingual** — Full Sinhala and English language support

---

## 🚨 Emergency Hotlines

| Service | Number |
|---|---|
| 🚑 Suwa Seriya Ambulance | **1990** |
| ℹ️ Health Information | **1979** |
| 🧠 Mental Health | **1926** |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, Vanilla JS (single-file) |
| Backend | Python / Flask |
| AI | [Groq API](https://console.groq.com) (free tier) |
| Data | CSV datasets (hospitals, medicines, symptoms, doctors) |

---

## 📁 Project Structure

```
suwa-sahaya/
├── index.html                  # Frontend — full UI in a single file
├── app.py                      # Flask backend — API + CSV loader
├── hospitals.csv               # Sri Lankan hospitals with contacts
├── medicine_alternatives.csv   # Brand vs generic medicine pricing
├── symptoms_conditions.csv     # Symptom → condition → urgency mapping
├── volunteer_doctors.csv       # Volunteer doctor profiles
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/suwa-sahaya.git
cd suwa-sahaya
```

### 2. Install dependencies

```bash
pip install flask groq
```

### 3. Run the server

```bash
python app.py
```

### 4. Open in browser

Visit **http://localhost:5000** and enter your Groq API key in the chat panel.

> **No `.env` file needed.** The Groq API key is entered directly in the browser — nothing is stored on the server.

---

## 🔑 Getting a Free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Create an API key (starts with `gsk_`)
4. Paste it into the chat panel on the app

---

## 🤖 AI Models Used (with auto-fallback)

The backend tries models in this order if one hits a rate limit:

1. `llama-3.1-8b-instant` — fastest, lowest token usage
2. `llama-3.3-70b-versatile` — smarter responses
3. `mixtral-8x7b-32768` — good fallback
4. `gemma2-9b-it` — last resort

---

## 📊 Data Sources

All CSV datasets are included in the repository and loaded at server startup. They cover:

- Government and private hospitals across Sri Lanka (by district)
- Common branded medicines and their affordable generic equivalents
- Symptom-to-condition mappings with home remedies and urgency levels
- Volunteer doctors with contact info, availability, and consultation type

---

## 🌍 Supported Districts

Colombo · Gampaha · Kandy · Galle · Matara · Kurunegala · Anuradhapura · Ratnapura · Badulla · Jaffna · Batticaloa · Trincomalee · Hambantota · Matale · Nuwara Eliya · Polonnaruwa · Ampara · Kegalle

---

## 🤝 Contributing

Contributions are welcome! Here are ways you can help:

- 📋 **Add data** — More hospitals, medicines, doctors, or symptom mappings to the CSV files
- 🌐 **Improve translations** — Better Sinhala or Tamil language support
- 🐛 **Report bugs** — Open an issue if you find something broken
- 💡 **Suggest features** — Open an issue with your idea

### To contribute:

```bash
git fork https://github.com/YOUR_USERNAME/suwa-sahaya.git
git checkout -b feature/your-feature-name
# make your changes
git commit -m "Add: description of your change"
git push origin feature/your-feature-name
# open a Pull Request
```

---

## ⚠️ Disclaimer

This application provides **health information only, not medical diagnoses**. Always consult a qualified healthcare professional for medical advice. In an emergency, call **1990** immediately.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<p align="center">Made with 💚 for the people of Sri Lanka</p>
