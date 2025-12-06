'use client';

import React from 'react';
import { cn } from '@/lib/utils';

export interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  children: React.ReactNode;
  required?: boolean;
}

export function Label({
  children,
  required,
  className,
  ...props
}: LabelProps) {
  return (
    <label
      className={cn(
        'text-body-regular',
        'text-text-primary',
        'font-regular',
        className
      )}
      {...props}
    >
      {children}
      {required && <span className="text-accent-red ml-1">*</span>}
    </label>
  );
}

