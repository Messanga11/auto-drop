/**
 * TypeScript types for DataTable component
 */

export interface ColumnDef<T> {
  key: string;
  label: string;
  render?: (item: T) => React.ReactNode;
  sortable?: boolean;
  width?: string;
}

export interface ActionDef<T> {
  label: string;
  onClick: (item: T) => void | Promise<void>;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: (item: T) => boolean;
  loading?: (item: T) => boolean;
}

export interface FilterConfig {
  key: string;
  label: string;
  type: 'text' | 'select' | 'date' | 'number' | 'boolean';
  options?: { value: string; label: string }[];
  placeholder?: string;
}

export interface DataTableProps<T> {
  // Données
  data: T[];
  columns: ColumnDef<T>[];
  
  // État
  loading: boolean;
  error: string | null;
  
  // Filtres
  filters?: FilterConfig[];
  onFilterChange?: (filters: Record<string, any>) => void;
  
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
  className?: string;
}

