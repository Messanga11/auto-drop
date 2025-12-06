'use client';

import { CreativeList } from '@/components/admin/CreativeList';
import { PageLayout } from '@/components/organisms/PageLayout/PageLayout';

export default function CreativesPage() {
  const token = typeof window !== 'undefined' ? localStorage.getItem('admin_token') : null;

  return (
    <PageLayout>
      <div className="space-y-section">
        <h1 className="text-title-xl font-extraLight mb-card text-text-primary">
          Créatifs
        </h1>
        <CreativeList token={token} />
      </div>
    </PageLayout>
  );
}
