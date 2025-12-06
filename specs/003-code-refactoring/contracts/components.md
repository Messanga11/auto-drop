# Component Contracts: Harmonisation du Code avec SOLID et DRY

**Feature**: 003-code-refactoring  
**Date**: 2024-12-19

## Overview

Ce document définit les contrats (interfaces) pour les composants et hooks génériques créés lors de la refactorisation. Ces contrats garantissent la compatibilité et la réutilisabilité.

## Frontend Component Contracts

### DataTable Component Contract

**File**: `frontend/src/components/common/DataTable/DataTable.tsx`

**Props Contract**:
```typescript
interface DataTableProps<T> {
  // Required
  data: T[];
  columns: ColumnDef<T>[];
  loading: boolean;
  error: string | null;
  pagination: PaginationState;
  onPageChange: (page: number) => void;
  onPageSizeChange: (pageSize: number) => void;
  
  // Optional
  filters?: FilterConfig[];
  onFilterChange?: (filters: Record<string, any>) => void;
  actions?: ActionDef<T>[];
  customFilters?: React.ReactNode;
  customActions?: (item: T) => React.ReactNode;
  emptyMessage?: string;
  className?: string;
}
```

**Behavior Contract**:
- Affiche un loader quand `loading === true`
- Affiche un message d'erreur quand `error !== null`
- Affiche les données dans un tableau avec les colonnes définies
- Affiche la pagination avec les contrôles page/page_size
- Appelle `onPageChange` quand l'utilisateur change de page
- Appelle `onPageSizeChange` quand l'utilisateur change la taille de page
- Affiche les filtres si `filters` est fourni
- Appelle `onFilterChange` quand un filtre change
- Affiche les actions pour chaque ligne si `actions` est fourni
- Affiche `customFilters` si fourni (remplace les filtres par défaut)
- Affiche `customActions(item)` pour chaque ligne si fourni
- Affiche `emptyMessage` si `data.length === 0` et `!loading`

**Performance Contract**:
- Utilise `React.memo` pour éviter les re-renders inutiles
- Utilise `useMemo` pour mémoriser les colonnes rendues
- Ne re-rend que quand les props changent (comparaison shallow)

### useDataList Hook Contract

**File**: `frontend/src/hooks/useDataList.ts`

**Input Contract**:
```typescript
function useDataList<T>(
  fetchFn: (filters: Record<string, any>, pagination: { page: number; page_size: number }) => Promise<{ items: T[]; total: number }>,
  wsHook: (token: string | null) => { items: T[]; setItems: (items: T[]) => void },
  token: string | null,
  initialFilters?: Record<string, any>
)
```

**Output Contract**:
```typescript
{
  data: T[];
  loading: boolean;
  error: string | null;
  filters: Record<string, any>;
  setFilters: (filters: Record<string, any>) => void;
  pagination: {
    page: number;
    page_size: number;
    total: number;
  };
  setPage: (page: number) => void;
  setPageSize: (pageSize: number) => void;
  refetch: () => Promise<void>;
}
```

**Behavior Contract**:
- Initialise `loading = true` au montage
- Appelle `fetchFn` avec les filtres et pagination initiaux
- Met à jour `data` avec les résultats de `fetchFn`
- Met à jour `loading = false` après le fetch (succès ou erreur)
- Met à jour `error` si le fetch échoue
- Synchronise `data` avec `wsHook.items` quand WebSocket envoie des mises à jour
- Appelle `fetchFn` automatiquement quand `filters` ou `pagination` change
- `refetch()` permet de recharger manuellement les données
- `setFilters()` met à jour les filtres et déclenche un nouveau fetch
- `setPage()` met à jour la page et déclenche un nouveau fetch
- `setPageSize()` met à jour la taille de page et déclenche un nouveau fetch

**Error Handling Contract**:
- Capture les erreurs de `fetchFn` et les met dans `error`
- Ne lance pas d'exception, retourne l'erreur dans `error`
- `error` est une string ou null

### ApiClient Service Contract

**File**: `frontend/src/lib/api/client.ts`

**Interface Contract**:
```typescript
class ApiClient {
  async request<T>(endpoint: string, options?: RequestInit): Promise<T>;
  async get<T>(endpoint: string, params?: Record<string, any>): Promise<T>;
  async post<T>(endpoint: string, data?: any): Promise<T>;
  async patch<T>(endpoint: string, data?: any): Promise<T>;
  async delete<T>(endpoint: string): Promise<T>;
  handleError(error: unknown): Error;
}
```

**Behavior Contract**:
- Toutes les méthodes ajoutent automatiquement le token d'authentification
- Toutes les méthodes gèrent les erreurs HTTP (401, 403, 404, 500, etc.)
- En cas de 401, supprime le token et redirige vers `/admin/login`
- `handleError` transforme toutes les erreurs en objets Error cohérents
- Les erreurs réseau sont capturées et transformées en Error avec message approprié

## Backend Helper Contracts

### Pagination Helper Contract

**File**: `backend/app/utils/pagination.py`

**Function Contracts**:
```python
def apply_pagination(query: Select, page: int, page_size: int) -> Select:
    """
    Contract:
    - Input: query SQLAlchemy, page >= 1, page_size >= 1
    - Output: query avec .offset() et .limit() appliqués
    - Raises: ValueError si page < 1 ou page_size < 1
    """
    pass

def get_total_count(query: Select, model: Type[Base]) -> int:
    """
    Contract:
    - Input: query SQLAlchemy, modèle SQLAlchemy
    - Output: nombre total d'éléments (int >= 0)
    - Preserves: tous les filtres de la query originale
    """
    pass
```

### Filtering Helper Contract

**File**: `backend/app/utils/filtering.py`

**Function Contract**:
```python
def apply_filters(
    query: Select,
    model: Type[Base],
    filters: Dict[str, Any]
) -> Select:
    """
    Contract:
    - Input: query SQLAlchemy, modèle, dictionnaire de filtres
    - Output: query avec filtres appliqués via .where()
    - Behavior: ignore les filtres pour des colonnes inexistantes
    - Raises: ValueError si le modèle n'a pas les colonnes spécifiées
    """
    pass
```

### Response Formatter Contract

**File**: `backend/app/utils/response.py`

**Function Contract**:
```python
def format_list_response(
    items: List[Any],
    total: int,
    page: int,
    page_size: int
) -> Dict[str, Any]:
    """
    Contract:
    - Input: liste d'items, total >= 0, page >= 1, page_size >= 1
    - Output: {
        "items": [...],
        "total": int,
        "page": int,
        "page_size": int
      }
    - Raises: ValueError si page < 1 ou page_size < 1
    """
    pass
```

### Error Handler Middleware Contract

**File**: `backend/app/middleware/error_handler.py`

**Class Contract**:
```python
class ErrorHandlerMiddleware:
    async def __call__(self, request: Request, call_next):
        """
        Contract:
        - Input: Request FastAPI, call_next function
        - Output: Response FastAPI
        - Behavior: 
          * Capture toutes les exceptions
          * Formate les erreurs de manière cohérente
          * Retourne JSON avec {"detail": "error message"} pour les erreurs
          * Log les erreurs avec le logger
        - Status codes:
          * 400 pour ValidationError
          * 401 pour AuthenticationError
          * 403 pour AuthorizationError
          * 404 pour NotFoundError
          * 500 pour autres erreurs
        """
        pass
```

## Compatibility Guarantees

### Backward Compatibility

- Les composants refactorisés (ProductList, CampaignList, etc.) doivent avoir exactement la même interface publique (mêmes props)
- Les routes backend refactorisées doivent avoir exactement la même interface API (mêmes endpoints, mêmes paramètres, mêmes réponses)
- Aucun breaking change pour les consommateurs existants

### Forward Compatibility

- Les abstractions (DataTable, useDataList, helpers) doivent être extensibles sans modification
- Nouveaux types de filtres/colonnes/actions peuvent être ajoutés via configuration
- Les helpers backend peuvent être étendus avec de nouveaux types de filtres sans modifier le code existant

