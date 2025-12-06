'use client';

import { useActionStatus } from '@/lib/websocket/hooks';
import { StatCard } from '@/components/molecules/StatCard/StatCard';

interface ActionStatusProps {
  token: string | null;
}

export function ActionStatus({ token }: ActionStatusProps) {
  const { scrapingStatus, scoringStatus, creativeStatus } =
    useActionStatus(token);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-gridGap">
      <StatCard
        title="Scraping"
        value={scrapingStatus?.status || 'Idle'}
        subtitle={scrapingStatus?.progress ? `${scrapingStatus.progress}%` : undefined}
      />
      <StatCard
        title="Scoring"
        value={scoringStatus?.status || 'Idle'}
        subtitle={scoringStatus?.progress ? `${scoringStatus.progress}%` : undefined}
      />
      <StatCard
        title="Créatifs"
        value={creativeStatus?.status || 'Idle'}
        subtitle={creativeStatus?.progress ? `${creativeStatus.progress}%` : undefined}
      />
    </div>
  );
}
