# Quickstart: Admin Dashboard Application

**Created**: 2024-12-04  
**Feature**: [spec.md](./spec.md)

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+ (ou SQLite pour développement)
- Redis 7.4+ (optionnel pour développement)

## Setup

### Backend

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env and set:
   # - DATABASE_URL
   # - ADMIN_DEFAULT_PASSWORD (optional, default: admin123)
   # - JWT_SECRET_KEY
   # - JWT_ALGORITHM (default: HS256)
   # - JWT_EXPIRATION_HOURS (default: 24)
   ```

3. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

4. **Start backend**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env.local
   # Edit .env.local and set:
   # - NEXT_PUBLIC_API_URL=http://localhost:8000
   # - NEXT_PUBLIC_WS_URL=ws://localhost:8000
   ```

3. **Start frontend**:
   ```bash
   npm run dev
   ```

## First Login

1. **Access admin login**:
   - URL: http://localhost:3000/admin/login

2. **Default credentials**:
   - Email: `admin@dropshipping.local`
   - Password: `admin123` (ou valeur de `ADMIN_DEFAULT_PASSWORD`)

3. **After login**:
   - Vous êtes redirigé vers le dashboard
   - La connexion WebSocket est établie automatiquement
   - L'indicateur de connexion affiche "Connected"

## Verify Installation

### Backend Health Check

```bash
curl http://localhost:8000/admin/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "websocket": "ready"
}
```

### Frontend Access

- Open http://localhost:3000/admin/login
- Login with default credentials
- Verify dashboard loads with metrics

### WebSocket Connection

1. Open browser DevTools → Network → WS
2. After login, verify WebSocket connection to `ws://localhost:8000/admin/ws?token=...`
3. Check for `{"type": "connected"}` message

## Common Issues

### Database Connection Error

**Problem**: `sqlalchemy.exc.OperationalError: could not connect to server`

**Solution**:
- Verify PostgreSQL is running: `pg_isready`
- Check `DATABASE_URL` in `.env`
- For SQLite dev: use `sqlite+aiosqlite:///./dropshipping.db`

### WebSocket Connection Failed

**Problem**: WebSocket connection fails with 1008 (Policy Violation)

**Solution**:
- Verify JWT token is valid and not expired
- Check token is correctly passed in query string
- Verify `JWT_SECRET_KEY` matches between backend and frontend

### Admin User Not Created

**Problem**: Cannot login with default credentials

**Solution**:
- Verify migrations ran: `alembic current`
- Check seed data was created: `SELECT * FROM admin_users WHERE email = 'admin@dropshipping.local';`
- Manually create admin if needed (see Troubleshooting)

## Troubleshooting

### Manually Create Admin User

```python
from app.models.admin import AdminUser
from app.database import SessionLocal
import bcrypt

db = SessionLocal()
password_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()

admin = AdminUser(
    email="admin@dropshipping.local",
    password_hash=password_hash,
    is_active=True
)
db.add(admin)
db.commit()
```

### Check WebSocket Events

1. Open browser DevTools → Console
2. Add WebSocket event listener:
   ```javascript
   // In browser console
   window.ws.addEventListener('message', (event) => {
     console.log('WebSocket event:', JSON.parse(event.data));
   });
   ```

### Verify Event Replay

1. Disconnect WebSocket (close browser tab)
2. Wait 10 seconds
3. Reconnect (open new tab and login)
4. Check console for replayed events

## Next Steps

- Review [data-model.md](./data-model.md) for entity details
- Check [contracts/api.yaml](./contracts/api.yaml) for API endpoints
- See [contracts/websocket.md](./contracts/websocket.md) for WebSocket events
- Read [research.md](./research.md) for implementation decisions

