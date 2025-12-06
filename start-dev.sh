#!/bin/bash

# Script de démarrage pour le développement

echo "🚀 Démarrage de la plateforme dropshipping en mode développement..."

# Backend
echo "📦 Démarrage du backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

# Vérifier que .env existe
if [ ! -f ".env" ]; then
    echo "⚠️  Fichier .env manquant. Création d'un .env par défaut..."
    cat > .env << 'EOF'
# Database - SQLite pour développement (pas besoin de PostgreSQL)
DATABASE_URL=sqlite+aiosqlite:///./dropshipping.db

# Redis (optionnel en développement)
REDIS_URL=redis://localhost:6379/0

# Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# Application
SECRET_KEY=dev-secret-key-change-in-production
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
EOF
fi

echo "✅ Backend prêt. Lancement sur http://localhost:8000"
echo "📚 Documentation API: http://localhost:8000/docs"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

BACKEND_PID=$!
cd ..

# Frontend
echo "🎨 Démarrage du frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installation des dépendances npm..."
    npm install
fi

# Vérifier que .env.local existe
if [ ! -f ".env.local" ]; then
    echo "⚠️  Fichier .env.local manquant. Création d'un .env.local par défaut..."
    cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WHATSAPP_NUMBER=237XXXXXXXXX
NEXT_PUBLIC_META_PIXEL_ID=your_pixel_id
NEXT_PUBLIC_TIKTOK_PIXEL_ID=your_tiktok_pixel
EOF
fi

echo "✅ Frontend prêt. Lancement sur http://localhost:3000"
npm run dev &

FRONTEND_PID=$!
cd ..

echo ""
echo "✨ Services démarrés!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter les services"

# Attendre les signaux
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait

