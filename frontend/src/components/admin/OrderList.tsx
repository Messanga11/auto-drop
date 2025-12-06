'use client';

/**
 * Order list component refactored to use DataTable and useDataList
 */

import { useState } from 'react';
import { Order } from '@/types/admin';
import * as adminApi from '@/lib/admin/api';
import { useOrders } from '@/lib/websocket/hooks';
import { useDataList } from '@/hooks/useDataList';
import { DataTable } from '@/components/common/DataTable/DataTable';
import { Select } from '@/components/atoms/Select/Select';
import { ColumnDef, FilterConfig } from '@/components/common/DataTable/types';

interface OrderListProps {
  token: string | null;
}

export function OrderList({ token }: OrderListProps) {
  const [actionLoading, setActionLoading] = useState<number | null>(null);

  // Use WebSocket hook directly
  const { orders: wsOrders, setOrders: setWsOrders } = useOrders(token);

  // Define columns for OrderList
  const columns: ColumnDef<Order>[] = [
    {
      key: 'id',
      label: 'ID',
    },
    {
      key: 'product_name',
      label: 'Produit',
    },
    {
      key: 'full_name',
      label: 'Client',
    },
    {
      key: 'phone',
      label: 'Téléphone',
    },
    {
      key: 'quantity',
      label: 'Quantité',
    },
    {
      key: 'status',
      label: 'Statut',
      render: (order) => (
        <span
          className={`px-2 py-1 rounded-full text-xs ${
            order.status === 'pending'
              ? 'bg-yellow-100 text-yellow-800'
              : order.status === 'confirmed'
              ? 'bg-blue-100 text-blue-800'
              : order.status === 'shipped'
              ? 'bg-purple-100 text-purple-800'
              : 'bg-green-100 text-green-800'
          }`}
        >
          {order.status}
        </span>
      ),
    },
    {
      key: 'created_at',
      label: 'Date',
      render: (order) => new Date(order.created_at).toLocaleDateString('fr-FR'),
    },
  ];

  // Define filters for OrderList
  const filterConfig: FilterConfig[] = [
    {
      key: 'status',
      label: 'Statut',
      type: 'select',
      options: [
        { value: 'pending', label: 'En attente' },
        { value: 'confirmed', label: 'Confirmé' },
        { value: 'shipped', label: 'Expédié' },
        { value: 'delivered', label: 'Livré' },
      ],
    },
    {
      key: 'date_from',
      label: 'Date de début',
      type: 'date',
    },
    {
      key: 'date_to',
      label: 'Date de fin',
      type: 'date',
    },
  ];

  // Fetch function for useDataList
  const fetchOrders = async (
    filters: Record<string, any>,
    pagination: { page: number; page_size: number }
  ) => {
    const response = await adminApi.getOrders({
      status: filters.status || undefined,
      date_from: filters.date_from || undefined,
      date_to: filters.date_to || undefined,
      page: pagination.page,
      page_size: pagination.page_size,
    });
    return {
      items: response.orders,
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
    refetch,
  } = useDataList<Order>({
    fetchFn: fetchOrders,
    wsItems: wsOrders,
    setWsItems: setWsOrders,
    token,
    initialFilters: {
      status: '',
      date_from: '',
      date_to: '',
    },
    initialPage: 1,
    initialPageSize: 20,
    queryKey: ['orders'], // Unique key for React Query
  });

  // Handle filter change
  const handleFilterChange = (newFilters: Record<string, any>) => {
    setFilters({ ...newFilters, page: 1 });
  };

  // Handle status update
  const handleStatusUpdate = async (order: Order, newStatus: string) => {
    if (!token) return;
    setActionLoading(order.id);
    try {
      await adminApi.updateOrderStatus(order.id, newStatus as any);
      await refetch();
    } catch (err) {
      console.error('Failed to update order status:', err);
    } finally {
      setActionLoading(null);
    }
  };

  // Define actions for OrderList
  const customActions = (order: Order) => (
    <Select
      options={[
        { value: 'pending', label: 'En attente' },
        { value: 'confirmed', label: 'Confirmé' },
        { value: 'shipped', label: 'Expédié' },
        { value: 'delivered', label: 'Livré' },
      ]}
      value={order.status}
      onChange={(e) => handleStatusUpdate(order, e.target.value)}
      disabled={actionLoading === order.id}
      className="w-40"
    />
  );

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
      customActions={customActions}
      emptyMessage="Aucune commande disponible"
    />
  );
}
