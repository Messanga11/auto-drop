'use client';

import { useState } from 'react';
import * as adminApi from '@/lib/admin/api';
import { Button } from '@/components/atoms/Button/Button';
import { ButtonGroup } from '@/components/molecules/ButtonGroup/ButtonGroup';

interface ActionButtonsProps {
  token: string | null;
  onActionTriggered?: () => void;
}

export function ActionButtons({
  token,
  onActionTriggered,
}: ActionButtonsProps) {
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleScraping = async (platform?: string) => {
    if (!token) return;
    setLoading('scraping');
    setError(null);
    try {
      await adminApi.startScraping(platform as 'facebook' | 'tiktok');
      onActionTriggered?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start scraping');
    } finally {
      setLoading(null);
    }
  };

  const handleScoring = async () => {
    if (!token) return;
    setLoading('scoring');
    setError(null);
    try {
      await adminApi.calculateScoring();
      onActionTriggered?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to calculate scoring');
    } finally {
      setLoading(null);
    }
  };

  if (error) {
    return (
      <div className="rounded-lg p-component bg-accent-red/20">
        <p className="text-body-small text-accent-red">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-card">
      <div>
        <h3 className="text-title-sm font-medium mb-component text-text-primary">
          Actions de scraping
        </h3>
        <ButtonGroup
          buttons={[
            {
              label: 'Scraper Facebook',
              onClick: () => handleScraping('facebook'),
              disabled: loading === 'scraping',
            },
            {
              label: 'Scraper TikTok',
              onClick: () => handleScraping('tiktok'),
              disabled: loading === 'scraping',
            },
          ]}
        />
      </div>

      <div>
        <h3 className="text-title-sm font-medium mb-component text-text-primary">
          Actions de scoring
        </h3>
        <Button
          onClick={handleScoring}
          disabled={loading === 'scoring' || !token}
        >
          {loading === 'scoring' ? 'Calcul en cours...' : 'Calculer les scores'}
        </Button>
      </div>
    </div>
  );
}
