'use client';

import { OrderList } from '@/components/admin/OrderList';
import { PageLayout } from '@/components/organisms/PageLayout/PageLayout';

export default function OrdersPage() {
  const token = typeof window !== 'undefined' ? localStorage.getItem('admin_token') : null;

  return (
    <PageLayout>
      <div className="space-y-section">
        <h1 className="text-title-xl font-extraLight mb-card text-text-primary">
          Commandes
        </h1>
        <OrderList token={token} />
      </div>
    </PageLayout>
  );
}
