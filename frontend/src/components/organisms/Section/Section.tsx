'use client';

import React from 'react';
import { tokens } from '@/design-system/tokens';
import { cn } from '@/lib/utils';

export interface SectionProps {
  children: React.ReactNode;
  withGlass?: boolean;
  className?: string;
}

export function Section({
  children,
  withGlass = false,
  className,
}: SectionProps) {
  return (
    <section
      className={cn(
        'p-section', // 32px padding
        withGlass && 'glass-card', // Apply glass effect if enabled
        className
      )}
    >
      {children}
    </section>
  );
}

