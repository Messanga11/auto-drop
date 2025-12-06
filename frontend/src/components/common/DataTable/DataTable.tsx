'use client';

/**
 * DataTable - Generic reusable table component for displaying data lists
 * with filters, pagination, loading, error handling, and actions
 */

import React, { useState, useEffect } from 'react';
import { DataTableProps, ColumnDef, ActionDef } from './types';
import { DataTableFilters } from './DataTableFilters';
import { DataTablePagination } from './DataTablePagination';
import { Badge } from '@/components/atoms/Badge/Badge';
import { cn } from '@/lib/utils';

export function DataTable<T extends Record<string, any>>({
  data,
  columns,
  loading,
  error,
  filters,
  onFilterChange,
  pagination,
  onPageChange,
  onPageSizeChange,
  actions,
  customFilters,
  customActions,
  emptyMessage = 'Aucune donnée disponible',
  className = '',
}: DataTableProps<T>) {
  // Manage local filter values - sync with parent when onFilterChange is called
  const [localFilterValues, setLocalFilterValues] = useState<Record<string, any>>({});

  // Sync local filter values when parent updates (via onFilterChange callback)
  useEffect(() => {
    if (onFilterChange) {
      // Parent manages filter state, we just display it
      // The parent will call onFilterChange with new values
    }
  }, [onFilterChange]);

  const handleFilterChange = (key: string, value: any) => {
    const newFilters = { ...localFilterValues, [key]: value };
    setLocalFilterValues(newFilters);
    if (onFilterChange) {
      onFilterChange(newFilters);
    }
  };

  const handleFilterReset = () => {
    const resetFilters: Record<string, any> = {};
    filters?.forEach((filter) => {
      resetFilters[filter.key] = filter.type === 'boolean' ? undefined : '';
    });
    setLocalFilterValues(resetFilters);
    if (onFilterChange) {
      onFilterChange(resetFilters);
    }
  };

  // Render cell content
  const renderCell = (item: T, column: ColumnDef<T>) => {
    if (column.render) {
      return column.render(item);
    }
    return item[column.key] ?? '-';
  };

  return (
    <div className={cn('space-y-gridGap', className)}>
      {/* Custom Filters or Default Filters - Only show when not loading to prevent hydration mismatch */}
      {!loading && (
        <>
          {customFilters ? (
            customFilters
          ) : filters && filters.length > 0 ? (
            <DataTableFilters
              filters={filters}
              values={localFilterValues}
              onChange={handleFilterChange}
              onReset={handleFilterReset}
            />
          ) : null}
        </>
      )}

      {/* Error Display */}
      {error && (
        <div className="rounded-lg p-card bg-accent-red/10 border border-accent-red/30">
          <p className="text-body-small text-accent-red">{error}</p>
        </div>
      )}

      {/* Table */}
      {loading ? (
        <div className="flex items-center justify-center py-section">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      ) : (
        <div className="glass-card rounded-lg overflow-hidden border border-background-glass shadow-soft">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-background-glassDark">
              <thead>
                <tr className="bg-background-glassDark/40">
                  {columns.map((column) => (
                    <th
                      key={column.key}
                      className={cn(
                        'px-card',
                        'py-component',
                        'text-left',
                        'text-body-small',
                        'font-medium',
                        'text-text-secondary',
                        'uppercase',
                        'tracking-wider',
                        'border-b',
                        'border-background-glassDark'
                      )}
                      style={column.width ? { width: column.width } : undefined}
                    >
                      {column.label}
                    </th>
                  ))}
                  {(actions && actions.length > 0) || customActions ? (
                    <th className="px-card py-component text-left text-body-small font-medium text-text-secondary uppercase tracking-wider border-b border-background-glassDark">
                      Actions
                    </th>
                  ) : null}
                </tr>
              </thead>
              <tbody className="divide-y divide-background-glassDark/50">
                {data.length === 0 ? (
                  <tr>
                    <td
                      colSpan={
                        columns.length + (actions && actions.length > 0 ? 1 : 0) + (customActions ? 1 : 0)
                      }
                      className="px-card py-section text-center"
                    >
                      <div className="flex flex-col items-center justify-center gap-component">
                        <p className="text-body-regular text-text-secondary">{emptyMessage}</p>
                      </div>
                    </td>
                  </tr>
                ) : (
                  data.map((item, index) => (
                    <tr
                      key={index}
                      className={cn(
                        'transition-colors duration-150',
                        'hover:bg-background-glassDark/20',
                        index % 2 === 0 ? 'bg-background-glassDark/5' : 'bg-transparent'
                      )}
                    >
                      {columns.map((column) => (
                        <td
                          key={column.key}
                          className={cn(
                            'px-card',
                            'py-component',
                            'text-body-regular',
                            'text-text-primary',
                            'whitespace-nowrap'
                          )}
                        >
                          {renderCell(item, column)}
                        </td>
                      ))}
                      {(actions && actions.length > 0) || customActions ? (
                        <td className="px-card py-component whitespace-nowrap">
                          <div className="flex items-center gap-component">
                            {actions?.map((action, actionIndex) => {
                              const isDisabled = action.disabled?.(item) || false;
                              const isLoading = action.loading?.(item) || false;
                              return (
                                <button
                                  key={actionIndex}
                                  onClick={() => !isDisabled && !isLoading && action.onClick(item)}
                                  disabled={isDisabled || isLoading}
                                  className={cn(
                                    'px-component',
                                    'py-1.5',
                                    'rounded-md',
                                    'text-body-small',
                                    'font-regular',
                                    'transition-all duration-150',
                                    action.variant === 'danger'
                                      ? 'bg-accent-red/20 text-accent-red hover:bg-accent-red/30'
                                      : action.variant === 'primary'
                                      ? 'bg-primary/20 text-primary hover:bg-primary/30'
                                      : 'bg-background-card text-text-primary hover:bg-background-glass',
                                    'disabled:opacity-50 disabled:cursor-not-allowed',
                                    'focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-background-dark'
                                  )}
                                >
                                  {isLoading ? '...' : action.label}
                                </button>
                              );
                            })}
                            {customActions && customActions(item)}
                          </div>
                        </td>
                      ) : null}
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {pagination.total > 0 && (
            <DataTablePagination
              page={pagination.page}
              page_size={pagination.page_size}
              total={pagination.total}
              onPageChange={onPageChange}
              onPageSizeChange={onPageSizeChange}
              loading={loading}
            />
          )}
        </div>
      )}
    </div>
  );
}

// Memoize the component to prevent unnecessary re-renders
export default React.memo(DataTable) as typeof DataTable;
