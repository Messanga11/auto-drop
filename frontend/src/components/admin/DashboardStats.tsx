'use client';

import { StatCard } from '@/components/molecules/StatCard/StatCard';
import { DashboardStats as DashboardStatsType } from '@/types/admin';

interface DashboardStatsProps {
  stats: DashboardStatsType | null;
}

export function DashboardStats({ stats }: DashboardStatsProps) {
  if (!stats) {
    return (
      <div className="text-body-regular text-text-secondary">
        Chargement des statistiques...
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-gridGap">
      <StatCard
        title="Produits totaux"
        value={stats.total_products || 0}
      />
      <StatCard
        title="Produits scorés"
        value={stats.scored_products || 0}
      />
      <StatCard
        title="Campagnes actives"
        value={stats.active_campaigns || 0}
      />
      <StatCard
        title="Commandes en attente"
        value={stats.pending_orders || 0}
      />
      <StatCard
        title="Total campagnes"
        value={stats.total_campaigns || 0}
      />
      <StatCard
        title="Total créatifs"
        value={stats.total_creatives || 0}
      />
    </div>
  );
}
