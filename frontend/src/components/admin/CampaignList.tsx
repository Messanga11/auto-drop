'use client';

/**
 * Campaign list component refactored to use DataTable and useDataList
 */

import { useState } from 'react';
import { Campaign } from '@/types/admin';
import * as adminApi from '@/lib/admin/api';
import { useCampaigns } from '@/lib/websocket/hooks';
import { useDataList } from '@/hooks/useDataList';
import { DataTable } from '@/components/common/DataTable/DataTable';
import { ColumnDef, FilterConfig } from '@/components/common/DataTable/types';

interface CampaignListProps {
  token: string | null;
}

export function CampaignList({ token }: CampaignListProps) {
  const [actionLoading, setActionLoading] = useState<number | null>(null);

  // Use WebSocket hook directly
  const { campaigns: wsCampaigns, setCampaigns: setWsCampaigns } = useCampaigns(token);

  // Define columns for CampaignList
  const columns: ColumnDef<Campaign>[] = [
    {
      key: 'id',
      label: 'ID',
    },
    {
      key: 'campaign_name',
      label: 'Nom',
      render: (campaign) => campaign.campaign_name || `Campagne #${campaign.id}`,
    },
    {
      key: 'platform',
      label: 'Plateforme',
    },
    {
      key: 'daily_budget',
      label: 'Budget',
      render: (campaign) => (campaign.daily_budget ? `$${campaign.daily_budget}` : '-'),
    },
    {
      key: 'status',
      label: 'Statut',
      render: (campaign) => (
        <span
          className={`px-2 py-1 rounded-full text-xs ${
            campaign.status === 'active'
              ? 'bg-green-100 text-green-800'
              : campaign.status === 'paused'
              ? 'bg-yellow-100 text-yellow-800'
              : 'bg-gray-100 text-gray-800'
          }`}
        >
          {campaign.status}
        </span>
      ),
    },
  ];

  // Define filters for CampaignList
  const filterConfig: FilterConfig[] = [
    {
      key: 'status',
      label: 'Statut',
      type: 'select',
      options: [
        { value: 'paused', label: 'Pause' },
        { value: 'active', label: 'Actif' },
        { value: 'completed', label: 'Terminé' },
      ],
    },
    {
      key: 'platform',
      label: 'Plateforme',
      type: 'select',
      options: [
        { value: 'meta', label: 'Meta' },
        { value: 'tiktok', label: 'TikTok' },
      ],
    },
  ];

  // Fetch function for useDataList
  const fetchCampaigns = async (
    filters: Record<string, any>,
    pagination: { page: number; page_size: number }
  ) => {
    const response = await adminApi.getCampaigns({
      status: filters.status || undefined,
      platform: filters.platform || undefined,
    });
    return {
      items: response.campaigns,
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
  } = useDataList<Campaign>({
    fetchFn: fetchCampaigns,
    wsItems: wsCampaigns,
    setWsItems: setWsCampaigns,
    token,
    initialFilters: {
      status: '',
      platform: '',
    },
    initialPage: 1,
    initialPageSize: 20,
    queryKey: ['campaigns'], // Unique key for React Query
  });

  // Handle filter change
  const handleFilterChange = (newFilters: Record<string, any>) => {
    setFilters({ ...newFilters, page: 1 });
  };

  // Handle activate/deactivate actions
  const handleActivate = async (campaign: Campaign) => {
    if (!token) return;
    setActionLoading(campaign.id);
    try {
      await adminApi.activateCampaign(campaign.id);
      await refetch();
    } catch (err) {
      console.error('Failed to activate campaign:', err);
    } finally {
      setActionLoading(null);
    }
  };

  const handleDeactivate = async (campaign: Campaign) => {
    if (!token) return;
    setActionLoading(campaign.id);
    try {
      await adminApi.deactivateCampaign(campaign.id);
      await refetch();
    } catch (err) {
      console.error('Failed to deactivate campaign:', err);
    } finally {
      setActionLoading(null);
    }
  };

  // Define actions for CampaignList
  const customActions = (campaign: Campaign) => (
    <>
      {campaign.status === 'active' ? (
        <button
          onClick={() => handleDeactivate(campaign)}
          disabled={actionLoading === campaign.id}
          className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-md hover:bg-yellow-200 disabled:opacity-50"
        >
          {actionLoading === campaign.id ? '...' : 'Désactiver'}
        </button>
      ) : (
        <button
          onClick={() => handleActivate(campaign)}
          disabled={actionLoading === campaign.id}
          className="px-3 py-1 bg-green-100 text-green-800 rounded-md hover:bg-green-200 disabled:opacity-50"
        >
          {actionLoading === campaign.id ? '...' : 'Activer'}
        </button>
      )}
    </>
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
      emptyMessage="Aucune campagne disponible"
    />
  );
}
