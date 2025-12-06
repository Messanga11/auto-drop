# Research: Admin Dashboard Application

**Created**: 2024-12-04  
**Feature**: [spec.md](./spec.md)

## Decisions & Rationale

### WebSocket Implementation

**Decision**: Utiliser `websockets` (Python) pour le serveur WebSocket backend et WebSocket API native (navigateur) pour le client frontend.

**Rationale**: 
- `websockets` est la bibliothèque Python standard pour WebSocket, compatible avec FastAPI via `fastapi-websocket` ou intégration native
- WebSocket API native du navigateur est supportée par tous les navigateurs modernes, pas besoin de dépendance externe
- Performance optimale avec async/await natif
- Compatible avec la stack FastAPI async

**Alternatives considered**:
- Socket.IO: Plus de fonctionnalités mais plus lourd, nécessite une dépendance supplémentaire côté client
- Server-Sent Events (SSE): Unidirectionnel uniquement, ne permet pas la communication bidirectionnelle requise
- Polling: Moins performant, génère plus de charge serveur

### WebSocket Authentication

**Decision**: Authentification via token JWT dans la query string lors de la connexion WebSocket (`ws://...?token=...`).

**Rationale**:
- Simple à implémenter et compatible avec la plupart des serveurs WebSocket
- Permet de rejeter immédiatement les connexions non authentifiées
- Token peut être récupéré depuis la session HTTP après login
- Sécurisé si le token est valide et non expiré

**Alternatives considered**:
- Token dans header HTTP: Certains proxies WebSocket peuvent ne pas transmettre les headers
- Message d'authentification après connexion: Nécessite de maintenir des connexions non authentifiées temporairement
- Cookie de session: Peut ne pas être transmis lors de l'upgrade WebSocket selon la configuration

### WebSocket Reconnection Strategy

**Decision**: Backoff exponentiel avec délai initial 500ms, maximum 60s, tentatives illimitées.

**Rationale**:
- Backoff exponentiel évite de surcharger le serveur lors de problèmes réseau temporaires
- Délai initial court (500ms) pour reconnexion rapide en cas de déconnexion brève
- Maximum 60s évite des tentatives trop espacées qui donneraient l'impression que l'application est cassée
- Tentatives illimitées garantissent que l'application se reconnecte toujours, même après des problèmes réseau prolongés

**Alternatives considered**:
- Tentatives limitées: Risque de laisser l'utilisateur avec une application déconnectée sans possibilité de reconnexion
- Reconnexion immédiate sans backoff: Peut surcharger le serveur en cas de problème réseau
- Backoff linéaire: Moins efficace que l'exponentiel pour gérer les problèmes réseau temporaires

### Event Replay Strategy

**Decision**: Rejouer tous les événements manqués depuis la dernière connexion lors de la reconnexion.

**Rationale**:
- Garantit la cohérence complète des données côté client
- L'administrateur ne manque aucune information importante
- Implémentation simple: stocker les événements avec timestamp et les rejouer lors de la reconnexion
- Performance acceptable pour un nombre limité d'administrateurs (5 max)

**Alternatives considered**:
- Rejouer uniquement les événements critiques: Risque de manquer des informations importantes
- Ne pas rejouer: Nécessite un rafraîchissement manuel, moins bonne expérience utilisateur
- Rejouer avec limite: Complexité supplémentaire pour déterminer quels événements sont importants

### Concurrent Modification Handling

**Decision**: Dernière modification gagne avec notification WebSocket aux autres administrateurs.

**Rationale**:
- Simple à implémenter et prévisible
- Évite les verrous qui peuvent bloquer les utilisateurs
- Notification WebSocket permet aux autres admins de voir les changements en temps réel
- Acceptable pour un nombre limité d'administrateurs (5 max)

**Alternatives considered**:
- Verrouillage optimiste: Plus complexe, nécessite gestion de conflits et confirmation utilisateur
- Verrouillage pessimiste: Peut bloquer les utilisateurs, moins adapté pour un petit nombre d'admins
- Fusion automatique: Très complexe, difficile à implémenter correctement

### Session Management

**Decision**: Sessions JWT avec expiration configurable, stockées en base de données (AdminSession).

**Rationale**:
- JWT permet de valider les sessions sans requête base de données à chaque requête
- Stockage en base permet de révoquer les sessions si nécessaire
- Expiration configurable pour sécurité
- Compatible avec authentification WebSocket (token dans query string)

**Alternatives considered**:
- Sessions uniquement en mémoire: Perdues au redémarrage du serveur
- Sessions uniquement en cookies: Moins flexible pour WebSocket
- Sessions Redis: Ajoute une dépendance, mais pourrait être considéré pour scale future

## Best Practices

### WebSocket Connection Management

- Maintenir une liste des connexions actives par administrateur
- Broadcast des événements à tous les administrateurs connectés
- Nettoyer les connexions fermées proprement
- Gérer les timeouts et les heartbeats pour détecter les connexions mortes

### Security

- Valider le token JWT à chaque connexion WebSocket
- Rejeter les connexions avec token invalide ou expiré
- Limiter le nombre de connexions par administrateur (1-2 max)
- Sanitizer les données envoyées via WebSocket

### Performance

- Utiliser async/await pour toutes les opérations WebSocket
- Éviter de bloquer le thread principal lors du broadcast
- Limiter la taille des messages WebSocket
- Compresser les messages si nécessaire pour les grandes listes

## Integration Points

### Backend Services

- `scraping_service.py`: Écouter les événements de scraping pour broadcast WebSocket
- `scoring_service.py`: Écouter les événements de scoring pour broadcast WebSocket
- `creative_service.py`: Écouter les événements de génération de créatives pour broadcast WebSocket
- `campaign_service.py`: Écouter les changements de statut de campagne pour broadcast WebSocket
- `order_service.py`: Écouter les nouvelles commandes et changements de statut pour broadcast WebSocket

### Frontend Integration

- Intégration avec les composants React existants (si applicable)
- Utilisation de React hooks pour gérer l'état WebSocket
- Context API pour partager l'état de connexion WebSocket entre composants

## References

- FastAPI WebSocket: https://fastapi.tiangolo.com/advanced/websockets/
- WebSocket API (MDN): https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- JWT Authentication: https://jwt.io/
- WebSocket Best Practices: https://www.nginx.com/blog/websocket-nginx/

