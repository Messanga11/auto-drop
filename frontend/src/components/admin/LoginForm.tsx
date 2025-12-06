'use client';

/**
 * Login form component for admin authentication.
 */

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/admin/AuthContext';
import { Form } from '@/components/molecules/Form/Form';
import { Button } from '@/components/atoms/Button/Button';
import { Card } from '@/components/molecules/Card/Card';

export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (data: Record<string, any>) => {
    setError(null);
    setLoading(true);

    try {
      await login(data.email || email, data.password || password);
      // Use window.location for a full page reload to ensure auth state is properly set
      window.location.href = '/admin/dashboard';
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur de connexion');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-screen">
      <Card variant="glass" className="w-full max-w-md">
        <div className="p-card space-y-section">
          <div>
            <h2 className="text-title-md font-regular text-center text-text-primary">
              Connexion Admin
            </h2>
            <p className="mt-2 text-center text-body-small text-text-secondary">
              Connectez-vous pour accéder au dashboard
            </p>
          </div>
          <Form onSubmit={handleSubmit}>
            {error && (
              <div className="rounded-lg p-component bg-accent-red/20">
                <p className="text-body-small text-accent-red">{error}</p>
              </div>
            )}
            <Form.Label required>Email</Form.Label>
            <Form.Input
              type="email"
              name="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <Form.Label required>Mot de passe</Form.Label>
            <Form.Input
              type="password"
              name="password"
              placeholder="Mot de passe"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <Form.Button type="submit" disabled={loading}>
              {loading ? 'Connexion...' : 'Se connecter'}
            </Form.Button>
          </Form>
        </div>
      </Card>
    </div>
  );
}
