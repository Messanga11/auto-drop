'use client';

import React, { useState } from 'react';
import { FilterConfig } from './types';
import { Input } from '@/components/atoms/Input/Input';
import { Select } from '@/components/atoms/Select/Select';
import { Checkbox } from '@/components/atoms/Checkbox/Checkbox';
import { Button } from '@/components/atoms/Button/Button';
import { Badge } from '@/components/atoms/Badge/Badge';
import { Icon } from '@/components/atoms/Icon/Icon';
import { Filter, X, ChevronDown, ChevronUp } from 'lucide-react';
import { cn } from '@/lib/utils';

interface DataTableFiltersProps {
  filters: FilterConfig[];
  values: Record<string, any>;
  onChange: (key: string, value: any) => void;
  onReset: () => void;
}

export function DataTableFilters({
  filters,
  values,
  onChange,
  onReset,
}: DataTableFiltersProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  
  // Check if any filter is active
  const activeFilters = Object.entries(values).filter(
    ([_, value]) => value !== '' && value !== undefined && value !== null && value !== false
  );
  const hasActiveFilters = activeFilters.length > 0;

  // Get active filter labels for display
  const getActiveFilterLabel = (key: string, value: any): string => {
    const filter = filters.find(f => f.key === key);
    if (!filter) return '';
    
    if (filter.type === 'select' && filter.options) {
      const option = filter.options.find(opt => String(opt.value) === String(value));
      return option ? option.label : value;
    }
    if (filter.type === 'boolean') {
      return filter.label;
    }
    return `${filter.label}: ${value}`;
  };

  return (
    <div className="flex flex-col gap-component">
      {/* Compact Filter Bar */}
      <div className="flex items-center gap-component flex-wrap">
        {/* Filter Button / Active Filters Display */}
        <div className="flex items-center gap-component flex-wrap">
          <Button
            variant="tag"
            state={isExpanded ? 'active' : 'inactive'}
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center gap-1.5"
          >
            <Icon icon={Filter} size={16} />
            <span>Filtres</span>
            {hasActiveFilters && (
              <Badge variant="tag" state="active" className="ml-1">
                {activeFilters.length}
              </Badge>
            )}
            <Icon icon={isExpanded ? ChevronUp : ChevronDown} size={14} />
          </Button>

          {/* Active Filter Tags */}
          {hasActiveFilters && (
            <>
              {activeFilters.map(([key, value]) => (
                <Badge
                  key={key}
                  variant="tag"
                  state="active"
                  className="flex items-center gap-1.5 pr-1"
                >
                  <span className="text-body-small">{getActiveFilterLabel(key, value)}</span>
                  <button
                    onClick={() => {
                      const filter = filters.find(f => f.key === key);
                      onChange(key, filter?.type === 'boolean' ? undefined : '');
                    }}
                    className="hover:opacity-70 transition-opacity"
                    aria-label="Supprimer le filtre"
                  >
                    <Icon icon={X} size={12} />
                  </button>
                </Badge>
              ))}
              
              {/* Clear All Button */}
              <button
                onClick={onReset}
                className="text-body-small text-text-secondary hover:text-text-primary transition-colors flex items-center gap-1"
              >
                <Icon icon={X} size={14} />
                <span>Tout effacer</span>
              </button>
            </>
          )}
        </div>
      </div>

      {/* Expanded Filters Panel */}
      {isExpanded && (
        <div className="glass-card rounded-lg p-component border border-background-glass">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-component">
            {filters.map((filter) => (
              <div key={filter.key} className="flex flex-col">
                {filter.type === 'text' && (
                  <Input
                    label={filter.label}
                    placeholder={filter.placeholder || filter.label}
                    value={values[filter.key] || ''}
                    onChange={(e) => onChange(filter.key, e.target.value)}
                  />
                )}
                {filter.type === 'number' && (
                  <Input
                    type="number"
                    label={filter.label}
                    placeholder={filter.placeholder || filter.label}
                    value={values[filter.key] || ''}
                    onChange={(e) => onChange(filter.key, e.target.value)}
                  />
                )}
                {filter.type === 'select' && filter.options && (
                  <Select
                    label={filter.label}
                    placeholder="Tous"
                    options={[
                      { value: '', label: 'Tous' },
                      ...filter.options.map(opt => ({ value: String(opt.value), label: opt.label }))
                    ]}
                    value={values[filter.key] || ''}
                    onChange={(e) => onChange(filter.key, e.target.value || undefined)}
                  />
                )}
                {filter.type === 'boolean' && (
                  <div className="pt-6">
                    <Checkbox
                      label={filter.label}
                      checked={values[filter.key] === true}
                      onChange={(e) => onChange(filter.key, e.target.checked || undefined)}
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
