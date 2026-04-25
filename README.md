# AYO 2.0 — Backend FastAPI + Groq
### IA officielle JOJ Dakar 2026

---

## 🚀 Déploiement GRATUIT en 5 minutes sur Render.com

### Étape 1 — Mettre le code sur GitHub

1. Va sur https://github.com et crée un compte (gratuit)
2. Clique **"New repository"** → nomme-le `ayo-backend`
3. Coche **"Add a README file"** → clique **"Create repository"**
4. Dans ton repo, clique **"Add file" → "Upload files"**
5. Glisse-dépose les 3 fichiers : `main.py`, `requirements.txt`, `render.yaml`
6. Clique **"Commit changes"**

---

### Étape 2 — Déployer sur Render (gratuit, sans carte bancaire)

1. Va sur https://render.com → **"Get Started for Free"**
2. Connecte-toi avec ton compte GitHub
3. Clique **"New +"** → **"Web Service"**
4. Sélectionne ton repo `ayo-backend`
5. Render détecte automatiquement la config. Vérifie :
   - **Runtime** : Python 3
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Clique **"Advanced"** → **"Add Environment Variable"**
   - Key : `GROQ_API_KEY`
   - Value : `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`
7. Clique **"Create Web Service"**
8. Attends ~2 minutes que le déploiement se termine ✅

---

### Étape 3 — Récupérer ton URL et mettre à jour le HTML

1. Dans le dashboard Render, copie l'URL de ton service
   (exemple : `https://ayo-2-joj-dakar.onrender.com`)
2. Dans le fichier `joj_connect_ayo.html`, trouve cette ligne :
   ```js
   const AYO_BACKEND_URL = 'http://127.0.0.1:8000';
   ```
3. Remplace-la par :
   ```js
   const AYO_BACKEND_URL = 'https://ayo-2-joj-dakar.onrender.com';
   ```
4. Sauvegarde et ouvre le HTML → AYO 2.0 répond ! 🎉

---

## ⚠️ Note importante sur la clé API Groq

La clé API visible dans ce projet (`gsk_yck...`) est exposée.
Il est recommandé de :
1. Aller sur https://console.groq.com → **"API Keys"** → **"Create API Key"**
2. Générer une **nouvelle clé**
3. L'utiliser dans Render comme variable d'environnement `GROQ_API_KEY`
4. Révoquer l'ancienne clé sur Groq Console

---

## 🔧 Lancer en local (pour tester)

```bash
pip install -r requirements.txt
export GROQ_API_KEY="ta_cle_groq"
uvicorn main:app --reload
```
Puis ouvre le HTML avec `AYO_BACKEND_URL = 'http://127.0.0.1:8000'`

---

## 📡 API

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/` | Statut du serveur |
| POST | `/chat` | Envoyer un message à AYO |

**Body /chat :**
```json
{
  "message": "Quels sports à la Tour de l'Œuf ?",
  "session_id": "optionnel-uuid-pour-continuer-la-conversation"
}
```

**Réponse :**
```json
{
  "reply": "La Tour de l'Œuf accueille 5 disciplines...",
  "session_id": "uuid-généré",
  "timestamp": "2026-04-25T10:30:00"
}
```
