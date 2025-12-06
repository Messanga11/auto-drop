'use client';

import React from 'react';
import { cn } from '@/lib/utils';

export interface BadgeProps {
  variant?: 'default' | 'tag';
  state?: 'active' | 'inactive';
  children: React.ReactNode;
  className?: string;
}

export function Badge({
  variant = 'default',
  state = 'inactive',
  children,
  className,
}: BadgeProps) {
  if (variant === 'tag') {
    const isActive = state === 'active';
    return (
      <span
        className={cn(
          'inline-flex items-center badge-tag font-regular',
          isActive ? 'badge-tag-active' : 'badge-tag-inactive',
          className
        )}
      >
        {children}
      </span>
    );
  }

  // Default variant
  return (
    <span
      className={cn(
        'inline-flex items-center',
        'font-regular',
        'rounded-md',
        'px-component',
        'py-1',
        'bg-background-card',
        'text-text-primary',
        className
      )}
    >
      {children}
    </span>
  );
}
