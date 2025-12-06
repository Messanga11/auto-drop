'use client';

import { useEffect } from 'react';
import { useAuth } from '@/lib/admin/AuthContext';
import { useDashboardStats } from '@/lib/websocket/hooks';
import { DashboardStats } from '@/components/admin/DashboardStats';
import { PageLayout } from '@/components/organisms/PageLayout/PageLayout';

export default function DashboardPage() {
  const { user } = useAuth();
  const token = typeof window !== 'undefined' ? localStorage.getItem('admin_token') : null;
  const { stats } = useDashboardStats(token);

  return (
    <PageLayout>
      <div className="space-y-section">
        <div>
          <h1 className="text-title-xl font-extraLight mb-card text-text-primary">
            Dashboard
          </h1>
          {user && (
            <p className="text-body-regular text-text-secondary">
              Bienvenue, {user.email}
            </p>
          )}
        </div>

        <DashboardStats stats={stats} />
      </div>
    </PageLayout>
  );
}
