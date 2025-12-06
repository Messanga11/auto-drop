'use client';

/**
 * Creative list component refactored to use DataTable and useDataList
 */

import { useState } from 'react';
import { Creative } from '@/types/admin';
import * as adminApi from '@/lib/admin/api';
import { useDataList } from '@/hooks/useDataList';
import { DataTable } from '@/components/common/DataTable/DataTable';
import { ColumnDef, FilterConfig } from '@/components/common/DataTable/types';

interface CreativeListProps {
  token: string | null;
}

export function CreativeList({ token }: CreativeListProps) {
  // Simple WebSocket hook wrapper (CreativeList doesn't use WebSocket yet)
  const wsItems: Creative[] = [];
  const setWsItems = () => {};

  // Define columns for CreativeList
  const columns: ColumnDef<Creative>[] = [
    {
      key: 'id',
      label: 'ID',
    },
    {
      key: 'product_id',
      label: 'Product ID',
    },
    {
      key: 'video_type',
      label: 'Type',
      render: (creative) => creative.video_type || '-',
    },
    {
      key: 'status',
      label: 'Statut',
      render: (creative) => (
        <span
          className={`px-2 py-1 rounded-full text-xs ${
            creative.status === 'completed'
              ? 'bg-green-100 text-green-800'
              : creative.status === 'processing'
              ? 'bg-blue-100 text-blue-800'
              : creative.status === 'failed'
              ? 'bg-red-100 text-red-800'
              : 'bg-gray-100 text-gray-800'
          }`}
        >
          {creative.status || 'unknown'}
        </span>
      ),
    },
    {
      key: 'created_at',
      label: 'Créé le',
      render: (creative) => new Date(creative.created_at).toLocaleDateString('fr-FR'),
    },
  ];

  // Define filters for CreativeList
  const filterConfig: FilterConfig[] = [
    {
      key: 'product_id',
      label: 'Product ID',
      type: 'number',
      placeholder: 'Filtrer par produit',
    },
    {
      key: 'status',
      label: 'Statut',
      type: 'select',
      options: [
        { value: 'queued', label: 'En attente' },
        { value: 'processing', label: 'En traitement' },
        { value: 'completed', label: 'Terminé' },
        { value: 'failed', label: 'Échoué' },
      ],
    },
  ];

  // Fetch function for useDataList
  const fetchCreatives = async (
    filters: Record<string, any>,
    pagination: { page: number; page_size: number }
  ) => {
    const response = await adminApi.getCreatives({
      product_id: filters.product_id ? parseInt(filters.product_id) : undefined,
      status: filters.status || undefined,
      page: pagination.page,
      page_size: pagination.page_size,
    });
    return {
      items: response.creatives,
      total: response.total,
    };
  };

  // Use useDataList hook with React Query
  const {
    data,
    loading,
    error,
    filters: filterValues,
    setFilters,
    pagination,
    setPage,
    setPageSize,
  } = useDataList<Creative>({
    fetchFn: fetchCreatives,
    wsItems,
    setWsItems,
    token,
    initialFilters: {
      product_id: '',
      status: '',
    },
    initialPage: 1,
    initialPageSize: 20,
    queryKey: ['creatives'], // Unique key for React Query
  });

  // Handle filter change
  const handleFilterChange = (newFilters: Record<string, any>) => {
    setFilters({ ...newFilters, page: 1 });
  };

  return (
    <DataTable
      data={data}
      columns={columns}
      loading={loading}
      error={error}
      filters={filterConfig}
      onFilterChange={handleFilterChange}
      pagination={pagination}
      onPageChange={setPage}
      onPageSizeChange={setPageSize}
      emptyMessage="Aucune créative disponible"
    />
  );
}
