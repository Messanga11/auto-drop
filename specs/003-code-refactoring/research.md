# Research: Harmonisation du Code avec SOLID et DRY

**Feature**: 003-code-refactoring  
**Date**: 2024-12-19

## Research Decisions

### Decision 1: Architecture du Composant DataTable Générique

**Decision**: Créer un composant DataTable hautement configurable avec un système de colonnes et d'actions personnalisables via props.

**Rationale**: 
- Les composants de liste partagent la même structure (filtres, pagination, chargement, erreurs, WebSocket sync) mais diffèrent dans les colonnes affichées et les actions disponibles
- Un composant générique avec configuration via props permet de réutiliser 80%+ du code tout en permettant la personnalisation
- Cette approche respecte le principe Open/Closed : ouvert à l'extension (nouvelles colonnes/actions) mais fermé à la modification

**Alternatives considered**:
- **Composition avec plusieurs petits composants**: Rejeté car cela créerait trop de complexité et de props à passer
- **HOC (Higher-Order Component)**: Rejeté car les Hooks sont plus modernes et flexibles dans React
- **Render props pattern**: Rejeté car moins lisible et plus verbeux que les props de configuration

**Implementation approach**:
- DataTable accepte un tableau de colonnes définies avec `key`, `label`, `render` (fonction optionnelle pour personnaliser le rendu)
- Actions personnalisables via `actions` prop (tableau d'actions avec `label`, `onClick`, `variant`)
- Filtres configurables via `filterConfig` prop
- WebSocket sync intégré via hook `useDataList`

### Decision 2: Architecture du Hook useDataList

**Decision**: Créer un hook générique `useDataList<T>` qui encapsule fetch, loading, error, pagination, filtres, et WebSocket sync.

**Rationale**:
- Tous les composants de liste répètent exactement le même pattern : useState pour data/loading/error/filters, useEffect pour fetch, useEffect pour WebSocket sync
- Un hook générique élimine cette duplication tout en permettant la personnalisation via des callbacks
- Respecte le principe Single Responsibility : le hook a une seule responsabilité (gestion de l'état et de la synchronisation des données)

**Alternatives considered**:
- **Service class**: Rejeté car les hooks React sont plus adaptés pour la gestion d'état dans les composants
- **Context API**: Rejeté car chaque liste a ses propres données, pas besoin de partage global
- **SWR/React Query**: Considéré mais rejeté car nécessite une dépendance externe et notre logique WebSocket est spécifique

**Implementation approach**:
- Hook générique avec type générique `<T>` pour la flexibilité
- Accepte une fonction `fetchFn` pour personnaliser l'appel API
- Accepte un hook WebSocket spécifique (useProducts, useCampaigns, etc.) pour la sync
- Retourne `{ data, loading, error, filters, setFilters, refetch, pagination }`

### Decision 3: Centralisation de la Logique Backend

**Decision**: Créer des helpers réutilisables dans `backend/app/utils/` pour pagination, filtrage, et formatage de réponses. Créer un middleware centralisé pour la gestion d'erreur.

**Rationale**:
- Les routes admin répètent les mêmes patterns : construction de query avec filtres, pagination, count total, formatage de réponse
- La centralisation permet d'éliminer la duplication et garantit la cohérence
- Respecte le principe DRY et Single Responsibility

**Alternatives considered**:
- **Base class pour routes**: Rejeté car FastAPI utilise des fonctions, pas des classes, et les décorateurs sont plus flexibles
- **Dependency injection avec classes**: Rejeté car ajoute de la complexité inutile
- **Decorators personnalisés**: Considéré mais rejeté car les helpers simples sont plus lisibles

**Implementation approach**:
- `utils/pagination.py`: Fonction `apply_pagination(query, page, page_size)` et `get_total_count(query)`
- `utils/filtering.py`: Fonction `apply_filters(query, model, filters_dict)` pour appliquer des filtres dynamiquement
- `utils/response.py`: Fonction `format_list_response(items, total, page, page_size)` pour standardiser les réponses
- `middleware/error_handler.py`: Middleware global pour capturer et formater les erreurs de manière cohérente

### Decision 4: Stratégie de Refactorisation Progressive

**Decision**: Refactoriser un composant à la fois (ProductList en premier) pour valider l'approche avant de généraliser.

**Rationale**:
- Réduit le risque de régression en testant chaque étape
- Permet d'ajuster l'approche si nécessaire avant de généraliser
- Facilite le review et la validation

**Alternatives considered**:
- **Refactorisation en une seule fois**: Rejeté car trop risqué et difficile à tester
- **Refactorisation parallèle**: Rejeté car si l'approche est incorrecte, il faudra tout refaire

**Implementation approach**:
1. Créer DataTable et useDataList
2. Refactoriser ProductList pour utiliser ces nouveaux composants
3. Tester exhaustivement ProductList
4. Refactoriser les autres composants un par un
5. Appliquer la même approche au backend

### Decision 5: Gestion des Cas Spécifiques

**Decision**: Utiliser le pattern "composition over configuration" pour les cas très spécifiques : permettre aux composants de surcharger des parties du DataTable via des props optionnelles.

**Rationale**:
- Certains composants peuvent avoir des besoins très spécifiques (par exemple, OrderList a des actions de mise à jour de statut)
- Plutôt que de rendre DataTable trop complexe, permettre la surcharge via des props optionnelles
- Respecte le principe Open/Closed : extension sans modification

**Alternatives considered**:
- **Tout rendre configurable**: Rejeté car rendrait DataTable trop complexe et difficile à maintenir
- **Créer des variantes spécialisées**: Rejeté car créerait de la duplication
- **Slots/Render props**: Considéré mais les props optionnelles sont plus simples

**Implementation approach**:
- DataTable accepte des props optionnelles pour surcharger des parties spécifiques
- Exemple : `customActions` prop pour ajouter des actions spécifiques au composant
- Exemple : `customFilters` prop pour des filtres très spécifiques
- Le composant peut toujours utiliser DataTable pour 80%+ de sa logique

## Technical Patterns

### Pattern 1: Generic React Component avec TypeScript

Utiliser les génériques TypeScript pour créer des composants type-safe mais flexibles :

```typescript
interface DataTableProps<T> {
  data: T[];
  columns: ColumnDef<T>[];
  loading: boolean;
  error: string | null;
  // ...
}
```

### Pattern 2: Custom Hooks pour Logique Réutilisable

Encapsuler la logique répétée dans des hooks personnalisés :

```typescript
function useDataList<T>(
  fetchFn: (filters: any) => Promise<{ items: T[]; total: number }>,
  wsHook: (token: string | null) => { items: T[]; setItems: (items: T[]) => void }
) {
  // Logique commune
}
```

### Pattern 3: Helper Functions pour Backend

Créer des fonctions utilitaires pures pour la logique répétée :

```python
def apply_pagination(query, page: int, page_size: int):
    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size)

def get_total_count(query, model):
    count_query = select(func.count()).select_from(model)
    # Appliquer les mêmes filtres
    return count_query
```

## Dependencies

Aucune nouvelle dépendance externe requise. Utilisation des technologies déjà en place :
- React 19+ (hooks, composants)
- TypeScript 5.6+ (génériques, types)
- FastAPI 0.115.0+ (décorateurs, dépendances)
- SQLAlchemy 2.0 (query building)

## Performance Considerations

- **Memoization**: Utiliser `React.memo` et `useMemo` dans DataTable pour éviter les re-renders inutiles
- **Lazy loading**: Les colonnes personnalisées peuvent être rendues de manière lazy si nécessaire
- **Query optimization**: Les helpers backend doivent optimiser les requêtes (éviter N+1 queries)

## Testing Strategy

- **Unit tests**: Tester les helpers backend et les hooks frontend isolément
- **Integration tests**: Tester que les composants refactorisés conservent exactement les mêmes fonctionnalités
- **Snapshot tests**: Comparer les snapshots avant/après refactorisation pour détecter les régressions visuelles

