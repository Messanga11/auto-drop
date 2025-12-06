'use client';

import { usePathname } from 'next/navigation';
import { AuthProvider } from '@/lib/admin/AuthContext';
import { ProtectedRoute } from '@/lib/admin/ProtectedRoute';
import { useWebSocket } from '@/lib/websocket/hooks';
import { ConnectionStatus } from '@/components/admin/ConnectionStatus';
import { ConflictNotification } from '@/components/admin/ConflictNotification';
import { useState, useEffect } from 'react';
import { useAuth } from '@/lib/admin/AuthContext';
import { Navbar } from '@/components/organisms/Navbar/Navbar';
import { Settings, BarChart3, Package, Megaphone, FileImage, ShoppingCart } from 'lucide-react';

function AdminNav() {
  const { user, logout } = useAuth();
  const pathname = usePathname();
  const token = typeof window !== 'undefined' ? localStorage.getItem('admin_token') : null;
  const { client, status } = useWebSocket(
    process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws/admin',
    token
  );
  const [conflictMessage, setConflictMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!client) return;

    const handleMessage = (event: { type: string; data?: any }) => {
      try {
        if (event.type === 'resource_conflict' || event.data?.conflict || event.data?.concurrent_modification) {
          setConflictMessage(
            event.data?.message || 'Une modification concurrente a été détectée. Veuillez rafraîchir la page.'
          );
        }
      } catch (e) {
        // Ignore parse errors
      }
    };

    const unsubscribe = client.onMessage(handleMessage);
    return () => {
      unsubscribe();
    };
  }, [client]);

  const navItems = [
    { label: 'Dashboard', href: '/admin/dashboard', icon: BarChart3 },
    { label: 'Produits', href: '/admin/products', icon: Package },
    { label: 'Campagnes', href: '/admin/campaigns', icon: Megaphone },
    { label: 'Créatifs', href: '/admin/creatives', icon: FileImage },
    { label: 'Commandes', href: '/admin/orders', icon: ShoppingCart },
    { label: 'Actions', href: '/admin/actions', icon: Settings },
  ];

  return (
    <>
      <Navbar
        user={user ? { name: user.email } : undefined}
        onLogout={logout}
        items={navItems}
      />
      <div className="pt-[68px]">
        {conflictMessage && (
          <div className="px-screen pt-section">
            <ConflictNotification
              message={conflictMessage}
              onDismiss={() => setConflictMessage(null)}
            />
          </div>
        )}
        <div className="fixed top-[72px] right-screen z-40 mt-2">
          <ConnectionStatus status={status} />
        </div>
      </div>
    </>
  );
}

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const isLoginPage = pathname === '/admin/login';

  return (
    <AuthProvider>
      {!isLoginPage && (
        <>
          <ProtectedRoute>
            <AdminNav />
          </ProtectedRoute>
        </>
      )}
      {children}
    </AuthProvider>
  );
}
