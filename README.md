# Chess Tutor Engine

Application web d'apprentissage des echecs avec un plateau interactif. Deplacez les pieces par glisser-deposer ou par clic.

## Pre-requis

- **Node.js** (v18 ou superieur)
- **npm** (inclus avec Node.js)
- **Python** 3.9 ou superieur
- **pip** (inclus avec Python)

## Structure du projet

```
chess-tutor-engine/
├── backend/          # API FastAPI (Python)
│   ├── app/main.py
│   ├── requirements.txt
│   └── start_server.py
├── frontend/         # Interface React (TypeScript)
│   ├── src/
│   │   ├── App.tsx        # Composant principal (plateau + logique)
│   │   └── App.css        # Styles
│   ├── package.json
│   └── tsconfig.json
└── README.md
```

## Installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd chess_tutor_engine
```

### 2. Backend (Python / FastAPI)

```bash
cd backend
pip install -r requirements.txt
```

### 3. Frontend (React / TypeScript)

```bash
cd frontend
npm install --legacy-peer-deps
```

> Le flag `--legacy-peer-deps` est necessaire pour eviter des conflits de versions entre les dependances.

## Lancement

### Demarrer le backend

```bash
cd backend
source .venv/bin/activate
python start_server.py
```

Le serveur API demarre sur `http://localhost:8000`.

Alternativement :

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Demarrer le frontend

Dans un autre terminal :

```bash
cd frontend
npm run dev
```

L'application s'ouvre sur `http://localhost:3000`.

## Build de production

```bash
cd frontend
npm run build
```

Les fichiers optimises sont generes dans le dossier `frontend/build/`.

Pour les servir localement :

```bash
npx serve -s build
```

## Commandes utiles

| Commande | Description |
|---|---|
| `npm start` | Lance le frontend en mode developpement |
| `npm run build` | Genere le build de production |
| `npm test` | Lance les tests frontend |
| `python start_server.py` | Demarre le backend avec rechargement automatique |
| `pip install -r requirements.txt` | Installe les dependances Python |
| `npm install --legacy-peer-deps` | Installe les dependances Node.js |

## Fonctionnalites

- Plateau d'echecs interactif (drag & drop + clic)
- Surbrillance des coups legaux
- Detection d'echec, echec et mat, match nul
- Annulation de coup
- Nouvelle partie
- Historique des coups joues

## Technologies

**Frontend :** React 18, TypeScript, react-chessboard, chess.js

**Backend :** FastAPI, python-chess, Uvicorn
