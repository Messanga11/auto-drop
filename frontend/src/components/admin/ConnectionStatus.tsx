'use client';

import { Badge } from '@/components/atoms/Badge/Badge';

interface ConnectionStatusProps {
  status: 'connected' | 'connecting' | 'disconnected' | 'reconnecting';
  isConnecting?: boolean;
}

export function ConnectionStatus({
  status = 'disconnected',
  isConnecting = false,
}: ConnectionStatusProps) {
  const getStatusLabel = () => {
    if (isConnecting || status === 'connecting' || status === 'reconnecting') return 'Connexion...';
    if (status === 'connected') return 'Connecté';
    return 'Déconnecté';
  };

  const getStatusVariant = (): 'active' | 'inactive' => {
    if (status === 'connected') return 'active';
    return 'inactive';
  };

  return (
    <Badge variant="tag" state={getStatusVariant()}>
      {getStatusLabel()}
    </Badge>
  );
}
