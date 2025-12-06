'use client';

/**
 * Product list component refactored to use DataTable and useDataList with React Query
 */

import { Product } from '@/types/admin';
import * as adminApi from '@/lib/admin/api';
import { useProducts } from '@/lib/websocket/hooks';
import { useDataList } from '@/hooks/useDataList';
import { DataTable } from '@/components/common/DataTable/DataTable';
import { ColumnDef, FilterConfig } from '@/components/common/DataTable/types';
import { Badge } from '@/components/atoms/Badge/Badge';

interface ProductListProps {
  token: string | null;
}

export function ProductList({ token }: ProductListProps) {
  // Use WebSocket hook directly
  const { products: wsProducts, setProducts: setWsProducts } = useProducts(token);

  // Define columns for ProductList
  const columns: ColumnDef<Product>[] = [
    {
      key: 'id',
      label: 'ID',
      width: '80px',
    },
    {
      key: 'platform',
      label: 'Plateforme',
      width: '120px',
      render: (product) => (
        <Badge variant="tag" state="inactive">
          {product.platform === 'facebook' ? 'Facebook' : product.platform === 'tiktok' ? 'TikTok' : product.platform}
        </Badge>
      ),
    },
    {
      key: 'page_name',
      label: 'Page/Advertiser',
      render: (product) => (
        <div className="flex flex-col gap-1">
          <div className="text-text-primary font-regular">{product.page_name || product.advertiser_name || '-'}</div>
          {product.caption && (
            <div className="text-body-small text-text-secondary truncate max-w-xs">
              {product.caption.substring(0, 60)}...
            </div>
          )}
        </div>
      ),
    },
    {
      key: 'engagement',
      label: 'Engagement',
      width: '180px',
      render: (product) => (
        <div className="flex flex-col gap-1">
          <div className="text-body-small text-text-secondary">
            <span className="text-text-primary font-medium">{product.likes || 0}</span> likes
          </div>
          <div className="text-body-small text-text-secondary">
            <span className="text-text-primary font-medium">{product.comments || 0}</span> comments
          </div>
          <div className="text-body-small text-text-secondary">
            <span className="text-text-primary font-medium">{product.views || 0}</span> views
          </div>
          {product.engagement_rate !== null && (
            <div className="text-body-small text-accent-green font-medium mt-1">
              {product.engagement_rate.toFixed(2)}%
            </div>
          )}
        </div>
      ),
    },
    {
      key: 'score',
      label: 'Score',
      width: '100px',
      render: (product) =>
        product.score !== null ? (
          <div className="flex items-center gap-1">
            <span className="text-title-sm font-medium text-primary">{product.score.toFixed(2)}</span>
          </div>
        ) : (
          <span className="text-body-small text-text-secondary">-</span>
        ),
    },
    {
      key: 'scored',
      label: 'Statut',
      width: '120px',
      render: (product) => (
        <Badge variant="tag" state={product.scored ? 'active' : 'inactive'}>
          {product.scored ? 'Scoré' : 'Non scoré'}
        </Badge>
      ),
    },
  ];

  // Define filters for ProductList
  const filterConfig: FilterConfig[] = [
    {
      key: 'platform',
      label: 'Plateforme',
      type: 'select',
      options: [
        { value: 'facebook', label: 'Facebook' },
        { value: 'tiktok', label: 'TikTok' },
      ],
    },
    {
      key: 'scored',
      label: 'Scoré',
      type: 'boolean',
    },
    {
      key: 'min_score',
      label: 'Score min',
      type: 'number',
      placeholder: '0.0',
    },
  ];

  // Fetch function for useDataList
  const fetchProducts = async (
    filters: Record<string, any>,
    pagination: { page: number; page_size: number }
  ) => {
    const response = await adminApi.getProducts({
      platform: filters.platform || undefined,
      scored: filters.scored,
      min_score: filters.min_score ? parseFloat(filters.min_score) : undefined,
      page: pagination.page,
      page_size: pagination.page_size,
    });
    return {
      items: response.products,
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
  } = useDataList<Product>({
    fetchFn: fetchProducts,
    wsItems: wsProducts,
    setWsItems: setWsProducts,
    token,
    initialFilters: {
      platform: '',
      scored: undefined,
      min_score: '',
    },
    initialPage: 1,
    initialPageSize: 20,
    queryKey: ['products'], // Unique key for React Query
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
      emptyMessage="Aucun produit disponible"
    />
  );
}
