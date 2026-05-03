"""
Suwa Sahaya - සුව සහාය | Free Healthcare AI Backend
Flask server — loads CSV datasets, calls Groq API using key sent from browser.
Rate-limit fix: compressed system prompt + model fallback + retry.
"""

import os, csv, time
from flask import Flask, request, jsonify, send_from_directory
from groq import Groq

app = Flask(__name__, static_folder=".")

# ── Load CSV data at startup ─────────────────────────────────────────────────
def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

BASE      = os.path.dirname(os.path.abspath(__file__))
HOSPITALS = load_csv(os.path.join(BASE, "hospitals.csv"))
MEDICINES = load_csv(os.path.join(BASE, "medicine_alternatives.csv"))
SYMPTOMS  = load_csv(os.path.join(BASE, "symptoms_conditions.csv"))
DOCTORS   = load_csv(os.path.join(BASE, "volunteer_doctors.csv"))

# ── Build COMPACT system prompt (fewer tokens = no rate limit) ───────────────
def build_system_prompt():

    # Only keep the most useful columns — keeps token count low
    def hospitals_text():
        lines = []
        for h in HOSPITALS:
            lines.append(
                f"{h['hospital_name']}|{h['district']}|{h['phone']}|"
                f"24hr:{h['emergency_24hr']}|{h['services']}"
            )
        return "\n".join(lines)

    def medicines_text():
        lines = []
        for m in MEDICINES:
            lines.append(
                f"{m['brand_name']}→{m['generic_name']}|{m['condition']}|"
                f"Brand:Rs{m['branded_price_LKR']} Generic:Rs{m['generic_price_LKR']}|"
                f"FreeGovt:{m['free_at_government_hospital']}"
            )
        return "\n".join(lines)

    def symptoms_text():
        lines = []
        for s in SYMPTOMS:
            lines.append(
                f"{s['symptoms']}→{s['possible_condition']}|"
                f"URGENCY:{s['urgency_level']}|"
                f"Remedy:{s['home_remedy']}|"
                f"SeeDoctor:{s['when_to_seek_help']}|"
                f"Specialist:{s['specialist_needed']}"
            )
        return "\n".join(lines)

    def doctors_text():
        lines = []
        for d in DOCTORS:
            lines.append(
                f"{d['name']}|{d['specialization']}|{d['district']} {d['area']}|"
                f"{d['available_days']} {d['available_time']}|"
                f"{d['consultation_type']}|📞{d['phone']}"
            )
        return "\n".join(lines)

    return f"""You are Suwa Sahaya 🌿, a healthcare AI for Sri Lanka. Answer using ONLY the datasets below.

=HOSPITALS=
{hospitals_text()}

=MEDICINES=
{medicines_text()}

=SYMPTOMS=
{symptoms_text()}

=DOCTORS=
{doctors_text()}

=RULES=
1. Symptoms → find match in SYMPTOMS → show: possible condition, urgency level, home remedy, when to see doctor, specialist needed
2. Medicine name → find in MEDICINES → show: generic name, generic price LKR, free at govt hospital yes/no
3. Doctor request → filter DOCTORS by specialization and/or district → list name, phone, days, time
4. Hospital request → filter HOSPITALS by district or service
5. EMERGENCY always → "📞 Call 1990 (Suwa Seriya Ambulance)"
6. Format with **bold** headers and emojis. Be warm and culturally sensitive.
7. If user writes in Sinhala → reply in Sinhala.
8. Always end with: ℹ️ This is health information only, not a medical diagnosis.
9. Key hotlines: Ambulance 1990 | Health Info 1979 | Mental Health 1926"""

SYSTEM_PROMPT = build_system_prompt()
TOKEN_ESTIMATE = len(SYSTEM_PROMPT) // 4
print(f"\n✅ System prompt ready — ~{TOKEN_ESTIMATE} tokens")
print(f"   {len(HOSPITALS)} hospitals | {len(MEDICINES)} medicines | "
      f"{len(SYMPTOMS)} symptoms | {len(DOCTORS)} doctors\n")

# ── Model fallback list (if one hits rate limit, try next) ───────────────────
MODELS = [
    "llama-3.1-8b-instant",       # fastest, lowest token usage — try first
    "llama-3.3-70b-versatile",    # smarter but more tokens
    "mixtral-8x7b-32768",         # good fallback
    "gemma2-9b-it",               # last resort
]

# ── Chat endpoint ────────────────────────────────────────────────────────────
@app.route("/api/chat", methods=["POST"])
def chat():
    data     = request.get_json(force=True)
    messages = data.get("messages", [])
    api_key  = data.get("api_key", "").strip()

    if not messages:
        return jsonify({"error": "No messages provided"}), 400
    if not api_key:
        return jsonify({"error": "API key not found. Please enter your Groq key in the chat panel."}), 400
    if not api_key.startswith("gsk_"):
        return jsonify({"error": "Invalid Groq API key format. Key should start with gsk_"}), 400

    groq_client = Groq(api_key=api_key)
    last_error  = ""

    for model in MODELS:
        try:
            response = groq_client.chat.completions.create(
                model=model,
                max_tokens=800,
                temperature=0.3,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages[-6:]
            )
            reply = response.choices[0].message.content
            return jsonify({"reply": reply, "model": model})

        except Exception as e:
            last_error = str(e)
            is_rate_limit = "429" in last_error or "rate_limit" in last_error.lower()
            is_auth       = "401" in last_error or "invalid_api_key" in last_error.lower() or "authentication" in last_error.lower()

            if is_auth:
                return jsonify({"error": "❌ Invalid Groq API key. Get a free key at console.groq.com"}), 401

            if is_rate_limit:
                # Wait briefly then try next model
                time.sleep(1)
                continue

            # Unknown error — try next model
            continue

    # All models failed
    return jsonify({
        "error": (
            "⚠️ All Groq models are rate limited right now.\n\n"
            "මෙය Groq free plan limit එකයි. විනාඩියකින් නැවත try කරන්න.\n\n"
            "Or get a paid Groq key at console.groq.com for higher limits.\n\n"
            "🚨 Emergency? Call 1990 (Suwa Seriya Ambulance)"
        )
    }), 429

# ── Data endpoints ────────────────────────────────────────────────────────────
@app.route("/api/doctors")
def get_doctors():
    district = request.args.get("district", "").lower()
    spec     = request.args.get("spec", "").lower()
    results  = DOCTORS
    if district:
        results = [d for d in results if district in d.get("district", "").lower()]
    if spec:
        results = [d for d in results if spec in d.get("specialization", "").lower()]
    return jsonify(results)

@app.route("/api/hospitals")
def get_hospitals():
    district = request.args.get("district", "").lower()
    results  = HOSPITALS
    if district:
        results = [h for h in results if district in h.get("district", "").lower()]
    return jsonify(results)

@app.route("/api/medicines")
def get_medicines():
    q       = request.args.get("q", "").lower()
    results = MEDICINES
    if q:
        results = [m for m in results if
                   q in m.get("brand_name", "").lower() or
                   q in m.get("generic_name", "").lower() or
                   q in m.get("condition", "").lower()]
    return jsonify(results)

# ── Serve frontend ────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    print("🌿 Suwa Sahaya starting on http://localhost:5000")
    print("   Enter your Groq API key in the browser — no terminal setup needed.\n")
    app.run(debug=True, port=5000)
