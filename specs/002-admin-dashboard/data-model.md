# Data Model: Admin Dashboard Application

**Created**: 2024-12-04  
**Feature**: [spec.md](./spec.md)

## Entities

### AdminUser (Compte Administrateur)

Représente un compte administrateur avec authentification.

**Fields**:
- `id` (Integer, PK): Identifiant unique
- `email` (String(255), UNIQUE, NOT NULL): Email de l'administrateur
- `password_hash` (String(255), NOT NULL): Hash du mot de passe (bcrypt)
- `is_active` (Boolean, default=True): Statut actif/inactif
- `created_at` (DateTime, default=now): Date de création
- `last_login_at` (DateTime, nullable): Date de dernière connexion
- `updated_at` (DateTime, default=now, onupdate=now): Date de dernière mise à jour

**Relationships**:
- One-to-Many avec `AdminSession` (un admin peut avoir plusieurs sessions)
- One-to-Many avec `AdminAction` (un admin peut effectuer plusieurs actions)

**Validation Rules**:
- `email` doit être unique et valide (format email)
- `password_hash` doit être un hash bcrypt valide
- `email` ne peut pas être modifié après création

**Indexes**:
- `idx_admin_user_email` sur `email` (UNIQUE)
- `idx_admin_user_active` sur `is_active`

**State Transitions**:
- `is_active=True` → `is_active=False` (désactivation)
- `is_active=False` → `is_active=True` (réactivation)

### AdminSession (Session d'Authentification)

Représente une session d'authentification active pour un administrateur.

**Fields**:
- `id` (Integer, PK): Identifiant unique
- `admin_id` (Integer, FK → AdminUser.id): Référence à l'administrateur
- `token` (String(512), UNIQUE, NOT NULL): Token JWT de la session
- `expires_at` (DateTime, NOT NULL): Date d'expiration de la session
- `ip_address` (String(45), nullable): Adresse IP de connexion (IPv4 ou IPv6)
- `user_agent` (String(255), nullable): User agent du navigateur
- `created_at` (DateTime, default=now): Date de création
- `last_used_at` (DateTime, default=now): Date de dernière utilisation

**Relationships**:
- Many-to-One avec `AdminUser` (une session appartient à un admin)

**Validation Rules**:
- `token` doit être unique
- `expires_at` doit être dans le futur lors de la création
- `admin_id` doit référencer un AdminUser existant et actif

**Indexes**:
- `idx_admin_session_token` sur `token` (UNIQUE)
- `idx_admin_session_admin` sur `admin_id`
- `idx_admin_session_expires` sur `expires_at` (pour nettoyage automatique)

**State Transitions**:
- Session créée → Session active → Session expirée (suppression automatique)
- Session peut être révoquée manuellement (suppression)

### AdminAction (Action Administrative)

Représente une action administrative effectuée par un administrateur (audit trail).

**Fields**:
- `id` (Integer, PK): Identifiant unique
- `admin_id` (Integer, FK → AdminUser.id): Référence à l'administrateur
- `action_type` (String(50), NOT NULL): Type d'action (ex: "scraping_started", "campaign_activated", "order_status_updated")
- `resource_type` (String(50), nullable): Type de ressource concernée (ex: "Campaign", "Order", "Product")
- `resource_id` (Integer, nullable): Identifiant de la ressource concernée
- `result` (String(20), NOT NULL): Résultat de l'action ("success", "failure", "partial")
- `details` (JSONB, nullable): Détails supplémentaires de l'action (métadonnées, erreurs)
- `created_at` (DateTime, default=now): Date de création

**Relationships**:
- Many-to-One avec `AdminUser` (une action appartient à un admin)

**Validation Rules**:
- `action_type` doit être un des types valides prédéfinis
- `result` doit être "success", "failure", ou "partial"
- `admin_id` doit référencer un AdminUser existant

**Indexes**:
- `idx_admin_action_admin` sur `admin_id`
- `idx_admin_action_type` sur `action_type`
- `idx_admin_action_resource` sur `resource_type`, `resource_id`
- `idx_admin_action_created` sur `created_at` (DESC pour historique récent)

**State Transitions**:
- Action créée → Action enregistrée (pas de modification après création)

## Relationships Summary

```
AdminUser (1) ──< (Many) AdminSession
AdminUser (1) ──< (Many) AdminAction
```

## Data Flow

1. **Authentification**: AdminUser créé → AdminSession créée avec token JWT → Token utilisé pour authentification WebSocket et API
2. **Actions**: AdminUser effectue action → AdminAction créée pour audit → Événement WebSocket broadcasté
3. **Sessions**: AdminSession créée → Utilisée pour authentification → Expire automatiquement ou révoquée manuellement

## Seed Data

### AdminUser par défaut

Lors de l'initialisation de la base de données, un compte admin par défaut est créé automatiquement:

- `email`: "admin@dropshipping.local"
- `password`: Configurable via variable d'environnement `ADMIN_DEFAULT_PASSWORD` (défaut: "admin123")
- `is_active`: True
- `created_at`: Date d'initialisation

**Note**: Le mot de passe par défaut DOIT être changé en production.

## Migration Notes

- Les tables `admin_users`, `admin_sessions`, et `admin_actions` sont créées via Alembic
- Index créés pour optimiser les requêtes fréquentes (email, token, dates)
- Contraintes de clé étrangère avec `ON DELETE CASCADE` pour AdminSession et AdminAction (si admin supprimé)

