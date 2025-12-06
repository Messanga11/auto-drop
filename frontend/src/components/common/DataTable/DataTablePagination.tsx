'use client';

import React from 'react';
import { Button } from '@/components/atoms/Button/Button';
import { Select } from '@/components/atoms/Select/Select';
import { Icon } from '@/components/atoms/Icon/Icon';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';

interface DataTablePaginationProps {
  page: number;
  page_size: number;
  total: number;
  onPageChange: (page: number) => void;
  onPageSizeChange: (pageSize: number) => void;
  loading?: boolean;
}

export function DataTablePagination({
  page,
  page_size,
  total,
  onPageChange,
  onPageSizeChange,
  loading,
}: DataTablePaginationProps) {
  const totalPages = Math.ceil(total / page_size);
  const startItem = (page - 1) * page_size + 1;
  const endItem = Math.min(page * page_size, total);

  return (
    <div className="px-card py-component bg-background-glassDark/20 border-t border-background-glassDark flex items-center justify-between">
      <div className="flex items-center gap-component">
        <span className="text-body-small text-text-secondary">
          Affichage de <span className="text-text-primary font-medium">{startItem}</span> à{' '}
          <span className="text-text-primary font-medium">{endItem}</span> sur{' '}
          <span className="text-text-primary font-medium">{total}</span>
        </span>
        <div className="flex items-center gap-component">
          <span className="text-body-small text-text-secondary">Par page:</span>
          <Select
            options={[
              { value: '10', label: '10' },
              { value: '20', label: '20' },
              { value: '50', label: '50' },
              { value: '100', label: '100' },
            ]}
            value={String(page_size)}
            onChange={(e) => onPageSizeChange(Number(e.target.value))}
            disabled={loading}
            className="w-20"
          />
        </div>
      </div>

      <div className="flex items-center gap-component">
        <Button
          variant="tag"
          state="inactive"
          onClick={() => onPageChange(page - 1)}
          disabled={page === 1 || loading}
        >
          <Icon icon={ChevronLeft} size={16} />
        </Button>
        <span className="text-body-regular text-text-primary min-w-[100px] text-center">
          Page <span className="font-medium">{page}</span> sur <span className="font-medium">{totalPages}</span>
        </span>
        <Button
          variant="tag"
          state="inactive"
          onClick={() => onPageChange(page + 1)}
          disabled={page >= totalPages || loading}
        >
          <Icon icon={ChevronRight} size={16} />
        </Button>
      </div>
    </div>
  );
}
