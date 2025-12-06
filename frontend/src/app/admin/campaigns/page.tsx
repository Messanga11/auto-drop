'use client';

import { CampaignList } from '@/components/admin/CampaignList';
import { PageLayout } from '@/components/organisms/PageLayout/PageLayout';

export default function CampaignsPage() {
  const token = typeof window !== 'undefined' ? localStorage.getItem('admin_token') : null;

  return (
    <PageLayout>
      <div className="space-y-section">
        <h1 className="text-title-xl font-extraLight mb-card text-text-primary">
          Campagnes
        </h1>
        <CampaignList token={token} />
      </div>
    </PageLayout>
  );
}
