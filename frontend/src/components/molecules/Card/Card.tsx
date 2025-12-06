'use client';

import React from 'react';
import { cn } from '@/lib/utils';

export interface CardProps {
  variant?: 'glass' | 'stat';
  children: React.ReactNode;
  className?: string;
}

export function Card({ variant = 'glass', children, className }: CardProps) {
  if (variant === 'stat') {
    return (
      <div className={cn('card-stat', className)}>
        {children}
      </div>
    );
  }

  // Glass variant
  return (
    <div className={cn('glass-card', className)}>
      {children}
    </div>
  );
}
