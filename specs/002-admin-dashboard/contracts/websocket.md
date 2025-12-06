# WebSocket API: Admin Dashboard

**Created**: 2024-12-04  
**Feature**: [spec.md](../spec.md)

## Connection

### Endpoint

```
ws://localhost:8000/admin/ws?token=<JWT_TOKEN>
```

### Authentication

- Le token JWT doit être fourni dans la query string `?token=...`
- Le token est obtenu après authentification via `/admin/auth/login`
- Les connexions sans token valide sont rejetées immédiatement

### Connection Flow

1. Client établit la connexion WebSocket avec token
2. Serveur valide le token
3. Si valide: connexion acceptée, message `{"type": "connected", "admin_id": <id>}`
4. Si invalide: connexion fermée avec code 1008 (Policy Violation)

## Message Format

Tous les messages sont au format JSON:

```json
{
  "type": "<event_type>",
  "timestamp": "2024-12-04T10:30:00Z",
  "data": { ... }
}
```

## Event Types

### Server → Client Events

#### `product_scraped`

Émis lorsqu'un nouveau produit est scrapé.

```json
{
  "type": "product_scraped",
  "timestamp": "2024-12-04T10:30:00Z",
  "data": {
    "product_id": 123,
    "platform": "facebook",
    "ad_id": "abc123"
  }
}
```

#### `product_scored`

Émis lorsqu'un produit est scoré.

```json
{
  "type": "product_scored",
  "timestamp": "2024-12-04T10:30:00Z",
  "data": {
    "product_id": 123,
    "score": 85.5,
    "rank": 3
  }
}
```

#### `creative_generated`

Émis lorsqu'une créative est générée.

```json
{
  "type": "creative_generated",
  "timestamp": "2024-12-04T10:30:00Z",
  "data": {
    "creative_id": 456,
    "product_id": 123,
    "video_type": "ugc",
    "status": "completed"
  }
}
```

#### `campaign_status_changed`

Émis lorsqu'une campagne change de statut.

```json
{
  "type": "campaign_status_changed",
  "timestamp": "2024-12-04T10:30:00Z",
  "data": {
    "campaign_id": 789,
    "product_id": 123,
    "platform": "meta",
    "old_status": "paused",
    "new_status": "active",
    "changed_by": 1
  }
}
```

#### `order_created`

Émis lorsqu'une nouvelle commande est créée.

```json
{
  "type": "order_created",
  "timestamp": "2024-12-04T10:30:00Z",
  "data": {
    "order_id": 101,
    "product_id": 123,
    "product_name": "Product Name",
    "status": "pending"
  }
}
```

#### `order_status_changed`

Émis lorsqu'une commande change de statut.

```json
{
  "type": "order_status_changed",
  "timestamp": "2024-12-04T10:30:00Z",
  "data": {
    "order_id": 101,
    "old_status": "pending",
    "new_status": "confirmed",
    "changed_by": 1
  }
}
```

#### `scraping_progress`

Émis pendant le scraping pour indiquer la progression.

```json
{
  "type": "scraping_progress",
  "timestamp": "2024-12-04T10:30:00Z",
  "data": {
    "progress": 45,
    "ads_scraped": 450,
    "total_expected": 1000
  }
}
```

#### `scraping_completed`

Émis lorsque le scraping est terminé.

```json
{
  "type": "scraping_completed",
  "timestamp": "2024-12-04T10:30:00Z",
  "data": {
    "ads_scraped": 1000,
    "duration_seconds": 3600
  }
}
```

#### `scoring_completed`

Émis lorsque le calcul des scores est terminé.

```json
{
  "type": "scoring_completed",
  "timestamp": "2024-12-04T10:30:00Z",
  "data": {
    "products_scored": 500,
    "top_5_products": [123, 456, 789, 101, 102]
  }
}
```

#### `dashboard_stats_updated`

Émis lorsque les métriques du dashboard sont mises à jour.

```json
{
  "type": "dashboard_stats_updated",
  "timestamp": "2024-12-04T10:30:00Z",
  "data": {
    "total_products": 1000,
    "scored_products": 500,
    "active_campaigns": 10,
    "pending_orders": 25
  }
}
```

#### `error`

Émis en cas d'erreur système.

```json
{
  "type": "error",
  "timestamp": "2024-12-04T10:30:00Z",
  "data": {
    "message": "Error message",
    "code": "ERROR_CODE",
    "details": {}
  }
}
```

### Client → Server Events

#### `ping`

Message de ping pour maintenir la connexion active.

```json
{
  "type": "ping"
}
```

Le serveur répond avec:

```json
{
  "type": "pong",
  "timestamp": "2024-12-04T10:30:00Z"
}
```

#### `request_replay`

Demande de rejeu des événements manqués depuis la dernière connexion.

```json
{
  "type": "request_replay",
  "data": {
    "since": "2024-12-04T09:00:00Z"
  }
}
```

Le serveur répond avec une série d'événements depuis la date spécifiée.

## Reconnection & Event Replay

### Automatic Reconnection

- Le client doit implémenter une reconnexion automatique avec backoff exponentiel
- Délai initial: 500ms
- Délai maximum: 60s
- Tentatives: illimitées

### Event Replay

Lors de la reconnexion:

1. Le client envoie `request_replay` avec `since` = timestamp de la dernière connexion
2. Le serveur envoie tous les événements depuis cette date
3. Les événements sont envoyés dans l'ordre chronologique
4. Après le rejeu, les événements en temps réel reprennent

## Connection Status

Le client doit afficher un indicateur visuel de l'état de connexion:

- **Connected**: Connexion active
- **Connecting**: Tentative de connexion en cours
- **Disconnected**: Déconnecté, reconnexion en cours
- **Error**: Erreur de connexion, afficher message d'erreur

## Error Handling

### Connection Errors

- **1008 (Policy Violation)**: Token invalide ou expiré → Rediriger vers login
- **1006 (Abnormal Closure)**: Connexion fermée anormalement → Tentative de reconnexion
- **1011 (Internal Error)**: Erreur serveur → Tentative de reconnexion avec backoff

### Message Errors

Si un message est malformé, le serveur ignore le message et continue.

## Best Practices

1. **Heartbeat**: Envoyer un `ping` toutes les 30 secondes pour maintenir la connexion
2. **Reconnection**: Toujours tenter de se reconnecter automatiquement
3. **Event Replay**: Toujours demander le rejeu des événements après reconnexion
4. **Error Handling**: Gérer gracieusement les erreurs de connexion
5. **State Management**: Maintenir l'état local et le synchroniser avec les événements WebSocket

