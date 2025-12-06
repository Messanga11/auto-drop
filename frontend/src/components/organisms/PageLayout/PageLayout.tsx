'use client';

import React from 'react';
import { tokens } from '@/design-system/tokens';
import { cn } from '@/lib/utils';

export interface PageLayoutProps {
  children: React.ReactNode;
  className?: string;
}

export function PageLayout({ children, className }: PageLayoutProps) {
  return (
    <div
      className={cn(
        'min-h-screen',
        'p-screen', // 48px padding
        className
      )}
    >
      <div
        className={cn(
          'mx-auto',
          'max-w-container', // 1600px
          className
        )}
      >
        {children}
      </div>
    </div>
  );
}

