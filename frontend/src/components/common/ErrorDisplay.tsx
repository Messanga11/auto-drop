'use client';

import { Card } from '@/components/molecules/Card/Card';
import { Icon } from '@/components/atoms/Icon/Icon';
import { AlertCircle } from 'lucide-react';

interface ErrorDisplayProps {
  error: string;
  title?: string;
  onRetry?: () => void;
}

export function ErrorDisplay({ error, title, onRetry }: ErrorDisplayProps) {
  return (
    <Card variant="glass" className="p-card bg-accent-red/20 border border-accent-red/50">
      <div className="flex items-start gap-component">
        <Icon icon={AlertCircle} size={24} className="text-accent-red flex-shrink-0" />
        <div className="flex-1">
          {title && (
            <h3 className="text-title-sm font-medium text-accent-red mb-1">
              {title}
            </h3>
          )}
          <p className="text-body-regular text-accent-red">{error}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-component text-body-small text-accent-red hover:text-accent-red/80 underline"
            >
              Réessayer
            </button>
          )}
        </div>
      </div>
    </Card>
  );
}
