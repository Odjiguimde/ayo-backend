"""
==============================================================
  AYO 2.0 — IA JOJ Dakar 2026
  Backend FastAPI + Groq (Llama 3.3)
==============================================================
"""
import os
import uuid
from datetime import datetime
from typing import Optional

from groq import Groq
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ─────────────────────────────
# 🔐 CONFIG GROQ
# La clé est lue depuis une variable d'environnement (sécurisé)
# ─────────────────────────────

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

# ─────────────────────────────
# APP FASTAPI
# ─────────────────────────────

app = FastAPI(title="AYO 2.0 IA")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────
# MÉMOIRE CONVERSATION
# ─────────────────────────────

conversations = {}

# ─────────────────────────────
# MODEL REQUEST
# ─────────────────────────────

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

# ─────────────────────────────
# PERSONNALITÉ IA
# ─────────────────────────────

SYSTEM_PROMPT = """
Tu es AYO 2.0, IA officielle des JOJ Dakar 2026.

Tu es une IA :
- conversationnelle et naturelle
- intelligente et chaleureuse
- multilingue : détecte automatiquement la langue de l'utilisateur et réponds dans cette même langue
  (français, anglais, wolof, espagnol, arabe, chinois, coréen, japonais, portugais...)

Tu aides sur :
- JOJ Dakar 2026 : 14 jours de compétition, du 31 octobre au 13 novembre 2026, environ 2 700 jeunes athlètes âgés de 14 à 18 ans, 25-26 disciplines sportives
- Sites officiels : Dakar (site principal), Saly (compétitions côtières) et Diamniadio (nouveau pôle sportif)
- Sites principaux: Tour de l'Œuf (piscine Olympique), Stade Iba Mar Diop, Corniche Ouest, Dakar Arena, Stade Abdoulaye Wade, CICAD, Centre Équestre de Diamniadio, Saly Plage Ouest
- Sport, transport, culture sénégalaise, infos pratiques
- Restaurants, hôtels, déplacements entre les sites
- Après l'événement : tu gardes vivante la mémoire des JOJ Dakar 2026

Réponds comme un humain chaleureux et enthousiaste, pas comme un bot.
Représente la culture sénégalaise avec fierté et bienveillance.
Célèbre la diversité culturelle : ces JOJ réunissent le monde entier.
Garde tes réponses concises (3-5 phrases max sauf si on te demande plus de détails).
"""

# ─────────────────────────────
# ROUTE CHAT
# ─────────────────────────────

@app.post("/chat")
def chat(payload: ChatMessage):

    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message vide")

    session_id = payload.session_id or str(uuid.uuid4())

    if session_id not in conversations:
        conversations[session_id] = []

    history = conversations[session_id]
    history.append({"role": "user", "content": payload.message})
    history = history[-20:]

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
            max_tokens=1024,
            temperature=0.8
        )
        reply = response.choices[0].message.content

    except Exception as e:
        print("ERREUR GROQ:", e)
        raise HTTPException(status_code=500, detail=str(e))

    history.append({"role": "assistant", "content": reply})
    conversations[session_id] = history

    return {
        "reply": reply,
        "session_id": session_id,
        "timestamp": datetime.now().isoformat()
    }

# ─────────────────────────────
# ROOT
# ─────────────────────────────

@app.get("/")
def root():
    return {"status": "AYO 2.0 active 🚀", "model": "llama-3.3-70b-versatile"}

# ─────────────────────────────
# RUN (local uniquement)
# ─────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
