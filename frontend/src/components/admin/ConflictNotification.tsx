'use client';

import { useState } from 'react';
import { Card } from '@/components/molecules/Card/Card';
import { Button } from '@/components/atoms/Button/Button';
import { Icon } from '@/components/atoms/Icon/Icon';
import { X } from 'lucide-react';

interface ConflictNotificationProps {
  message: string;
  onDismiss?: () => void;
}

export function ConflictNotification({
  message,
  onDismiss,
}: ConflictNotificationProps) {
  const [dismissed, setDismissed] = useState(false);

  if (dismissed) return null;

  const handleDismiss = () => {
    setDismissed(true);
    onDismiss?.();
  };

  return (
    <Card variant="glass" className="p-card bg-accent-red/20 border border-accent-red/50">
      <div className="flex items-start justify-between gap-component">
        <div className="flex-1">
          <p className="text-body-regular text-accent-red">{message}</p>
        </div>
        <Button
          variant="tag"
          onClick={handleDismiss}
          className="p-1"
          aria-label="Fermer"
        >
          <Icon icon={X} size={16} />
        </Button>
      </div>
    </Card>
  );
}
