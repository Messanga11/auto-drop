'use client';

import React from 'react';
import { Card } from '@/components/molecules/Card/Card';
import { cn } from '@/lib/utils';

export interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  className?: string;
}

export function StatCard({
  title,
  value,
  subtitle,
  className,
}: StatCardProps) {
  return (
    <Card variant="stat" className={cn(className)}>
      <div className="flex flex-col">
        <p className="text-body-small text-text-secondary mb-1">{title}</p>
        <p className="text-title-md font-regular text-text-primary">
          {value}
        </p>
        {subtitle && (
          <p className="text-body-small text-text-secondary mt-1">
            {subtitle}
          </p>
        )}
      </div>
    </Card>
  );
}

