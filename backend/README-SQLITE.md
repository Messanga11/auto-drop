# Configuration SQLite pour le développement

Le projet utilise **SQLite** par défaut en développement, ce qui simplifie grandement le setup.

## Avantages

- ✅ **Aucune installation** : SQLite est inclus avec Python
- ✅ **Aucune configuration** : Pas besoin de serveur de base de données
- ✅ **Fichier unique** : Toutes les données dans `dropshipping.db`
- ✅ **Développement rapide** : Démarrage instantané

## Configuration

Le fichier `.env` contient déjà la configuration SQLite :

```env
DATABASE_URL=sqlite+aiosqlite:///./dropshipping.db
```

## Migrations

Les migrations Alembic sont compatibles avec SQLite et PostgreSQL :

```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

## Production

Pour la production, changez simplement `DATABASE_URL` dans `.env` :

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dropshipping
```

Le code s'adapte automatiquement !

## Fichier de base de données

- **Localisation** : `backend/dropshipping.db`
- **Taille** : ~66KB initialement
- **Git** : Exclu du dépôt (dans `.gitignore`)

## Vérification

Pour vérifier que tout fonctionne :

```bash
# Vérifier les tables
sqlite3 backend/dropshipping.db ".tables"

# Voir le schéma
sqlite3 backend/dropshipping.db ".schema"
```

