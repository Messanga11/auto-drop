'use client';

/**
 * Admin login page.
 */

import { LoginForm } from '@/components/admin/LoginForm';
import { AuthProvider } from '@/lib/admin/AuthContext';

export default function LoginPage() {
  return (
    <AuthProvider>
      <LoginForm />
    </AuthProvider>
  );
}
