'use client';

import { ActionButtons } from '@/components/admin/ActionButtons';
import { ActionStatus } from '@/components/admin/ActionStatus';
import { PageLayout } from '@/components/organisms/PageLayout/PageLayout';

export default function ActionsPage() {
  const token = typeof window !== 'undefined' ? localStorage.getItem('admin_token') : null;

  return (
    <PageLayout>
      <div className="space-y-section">
        <h1 className="text-title-xl font-extraLight mb-card text-text-primary">
          Actions
        </h1>
        <div className="space-y-section">
          <ActionButtons token={token} />
          <ActionStatus token={token} />
        </div>
      </div>
    </PageLayout>
  );
}
