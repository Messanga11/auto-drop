# Data Model: Harmonisation du Code avec SOLID et DRY

**Feature**: 003-code-refactoring  
**Date**: 2024-12-19

## Overview

Cette refactorisation n'introduit pas de nouvelles entités de données dans la base de données. Elle se concentre sur la création d'abstractions et d'interfaces pour éliminer la duplication de code. Ce document décrit les abstractions et interfaces créées.

## Frontend Abstractions

### DataTable Component Interface

**Purpose**: Composant générique réutilisable pour tous les tableaux de données

**Props Interface**:
```typescript
interface DataTableProps<T> {
  // Données
  data: T[];
  columns: ColumnDef<T>[];
  
  // État
  loading: boolean;
  error: string | null;
  
  // Filtres
  filters: FilterConfig[];
  onFilterChange: (filters: Record<string, any>) => void;
  
  // Pagination
  pagination: {
    page: number;
    page_size: number;
    total: number;
  };
  onPageChange: (page: number) => void;
  onPageSizeChange: (pageSize: number) => void;
  
  // Actions (optionnel)
  actions?: ActionDef<T>[];
  
  // Personnalisation (optionnel)
  customFilters?: React.ReactNode;
  customActions?: (item: T) => React.ReactNode;
  emptyMessage?: string;
}
```

**Column Definition**:
```typescript
interface ColumnDef<T> {
  key: string;
  label: string;
  render?: (item: T) => React.ReactNode;
  sortable?: boolean;
  width?: string;
}
```

**Action Definition**:
```typescript
interface ActionDef<T> {
  label: string;
  onClick: (item: T) => void | Promise<void>;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: (item: T) => boolean;
  loading?: (item: T) => boolean;
}
```

**Filter Configuration**:
```typescript
interface FilterConfig {
  key: string;
  label: string;
  type: 'text' | 'select' | 'date' | 'number' | 'boolean';
  options?: { value: string; label: string }[];
  placeholder?: string;
}
```

### useDataList Hook Interface

**Purpose**: Hook générique pour gérer l'état et la synchronisation des données de liste

**Interface**:
```typescript
function useDataList<T>(
  fetchFn: (filters: Record<string, any>, pagination: { page: number; page_size: number }) => Promise<{ items: T[]; total: number }>,
  wsHook: (token: string | null) => { items: T[]; setItems: (items: T[]) => void },
  token: string | null,
  initialFilters?: Record<string, any>
): {
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

**Responsibilities**:
- Gérer l'état loading/error
- Gérer les filtres et la pagination
- Appeler fetchFn avec les filtres/pagination actuels
- Synchroniser avec WebSocket via wsHook
- Fournir refetch pour recharger les données

### API Client Service Interface

**Purpose**: Service centralisé pour toutes les communications avec le backend

**Interface**:
```typescript
class ApiClient {
  private baseUrl: string;
  private getToken: () => string | null;
  
  async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T>;
  
  async get<T>(endpoint: string, params?: Record<string, any>): Promise<T>;
  async post<T>(endpoint: string, data?: any): Promise<T>;
  async patch<T>(endpoint: string, data?: any): Promise<T>;
  async delete<T>(endpoint: string): Promise<T>;
  
  // Error handling
  handleError(error: unknown): Error;
}
```

## Backend Abstractions

### Pagination Helper Interface

**Purpose**: Helper pour appliquer la pagination aux requêtes SQLAlchemy

**Interface**:
```python
def apply_pagination(
    query: Select,
    page: int,
    page_size: int
) -> Select:
    """
    Applique la pagination à une requête SQLAlchemy.
    
    Returns:
        Query avec offset et limit appliqués
    """
    pass

def get_total_count(
    query: Select,
    model: Type[Base]
) -> int:
    """
    Calcule le nombre total d'éléments pour une requête.
    
    Returns:
        Nombre total d'éléments
    """
    pass
```

### Filtering Helper Interface

**Purpose**: Helper pour appliquer des filtres dynamiquement aux requêtes

**Interface**:
```python
def apply_filters(
    query: Select,
    model: Type[Base],
    filters: Dict[str, Any]
) -> Select:
    """
    Applique des filtres dynamiquement à une requête.
    
    Args:
        query: Requête SQLAlchemy de base
        model: Modèle SQLAlchemy
        filters: Dictionnaire de filtres {field: value}
    
    Returns:
        Query avec filtres appliqués
    """
    pass
```

### Response Formatter Interface

**Purpose**: Helper pour formater les réponses de liste de manière cohérente

**Interface**:
```python
def format_list_response(
    items: List[Any],
    total: int,
    page: int,
    page_size: int
) -> Dict[str, Any]:
    """
    Formate une réponse de liste avec pagination.
    
    Returns:
        {
            "items": [...],
            "total": int,
            "page": int,
            "page_size": int
        }
    """
    pass
```

### Error Handler Middleware

**Purpose**: Middleware centralisé pour la gestion d'erreur

**Interface**:
```python
class ErrorHandlerMiddleware:
    """
    Middleware pour capturer et formater les erreurs de manière cohérente.
    """
    
    async def __call__(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # Formater l'erreur de manière cohérente
            return format_error_response(e)
```

## Relationships

- **DataTable** utilise **useDataList** pour gérer l'état
- **useDataList** utilise **ApiClient** pour les appels API
- **useDataList** utilise les hooks WebSocket spécifiques (useProducts, useCampaigns, etc.) pour la synchronisation
- Les routes backend utilisent les helpers (pagination, filtering, response) pour éliminer la duplication
- Le middleware ErrorHandler capture toutes les erreurs des routes

## Validation Rules

- **DataTable**: Les colonnes doivent avoir une `key` unique. Les actions doivent avoir un `label` et un `onClick`.
- **useDataList**: `fetchFn` doit retourner un objet avec `items` et `total`. `wsHook` doit retourner un objet avec `items` et `setItems`.
- **Backend helpers**: Les filtres doivent correspondre à des colonnes existantes du modèle. La pagination doit avoir `page >= 1` et `page_size >= 1`.

## State Transitions

N/A - Ce sont des abstractions, pas des entités avec état.

